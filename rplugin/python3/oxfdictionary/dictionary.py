import json
import math
import os
import pickle
import typing
import copy

import requests


class Dict:
    def __init__(self, nvim) -> None:
        self._nvim = nvim
        self._app_id = nvim.eval("g:OxfDictionary#app_id")
        self._app_key = nvim.eval("g:OxfDictionary#app_key")
        self._f_win_max_width = 101
        self._cache_path = (
            os.path.dirname(os.path.abspath(__file__)) + "/dict_cache.dump"
        )

    def _error(self, msg: str) -> None:
        self._nvim.call("oxfdictionary#print_error", msg)

    def _get_word(self, arg: typing.List[str]) -> str:
        if arg:
            word = arg[0]
        else:
            word = self._nvim.eval('expand("<cword>")')
        return word.lower()

    def _check_dump(self, word: str) -> typing.List[str]:
        # check if the selected word is cached
        definitions = []
        if (os.path.exists(self._cache_path) and
                os.path.getsize(self._cache_path)):
            cache_file = open(self._cache_path, "rb")
            word_dict = pickle.load(cache_file)
            cache_file.close()
            definitions = word_dict.get(word, [])
        return definitions

    def _update_dump(self, word: str, defs: typing.List[str]) -> None:
        if not os.path.exists(self._cache_path):
            os.system("touch {}".format(self._cache_path))
        wordList = {}
        if os.path.getsize(self._cache_path):
            cache_file = open(self._cache_path, "rb")
            wordList = pickle.load(cache_file)
            cache_file.close()

        wordList[word] = defs
        cacheFile = open(self._cache_path, "wb")
        pickle.dump(wordList, cacheFile)
        cacheFile.close()

    def _get_api_msg(self, word_id: str):
        base_url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/"
        url = (
            base_url
            + "en-us"
            + "/"
            + word_id
            + "?fields="
            + "definitions"
            + "&strictMatch="
            + "false"
        )
        return requests.get(
            url, headers={"app_id": self._app_id, "app_key": self._app_key}
        )

    def _process_def_dict(self, def_dict: dict) -> typing.List[str]:
        definitions = []
        for jresult in def_dict["results"]:
            for jle in jresult["lexicalEntries"]:
                lCategory = jle["lexicalCategory"]["text"]
                definitions.append(lCategory)
                for ent in jle["entries"]:
                    for sen in ent["senses"]:
                        for defn in sen["definitions"]:
                            definitions.append("- " + defn)
        return definitions

    def _get_f_win_size(
            self, lines: typing.List[str]) -> typing.Tuple[int, int]:
        height = 0
        width = 10
        for line in lines:
            width = max(width, min(len(line), self._f_win_max_width))
            height += \
                1 + math.floor((len(line) - 1) / (self._f_win_max_width - 1))
        return height, width

    def _show_floating_window(
            self, word: str, lines: typing.List[str]) -> None:
        lines.insert(0, word)
        [win_height, win_width] = self._get_f_win_size(lines)
        cursor_row = self._nvim.call("oxfdictionary#get_cursor_pos_in_screen")
        screen_height = self._nvim.eval("&lines")

        if cursor_row > screen_height / 2:
            anchor = "SW"
            fwin_row = max(win_height, cursor_row - 1)
        else:
            anchor = "NW"
            fwin_row = min(screen_height - win_height, cursor_row)

        new_buf_nr: int = self._nvim.call("nvim_create_buf", False, True)
        self._nvim.call(
            "nvim_open_win",
            new_buf_nr,
            True,
            {
                "relative": "editor",
                "row": fwin_row,
                "col": 15,
                "width": win_width + 1,
                "height": win_height,
                "anchor": anchor,
            },
        )
        self._nvim.command("setlocal nonumber")
        self._nvim.command(
            "nnoremap <buffer><silent> q :call nvim_win_close(0, 0)<CR>"
        )
        buffer = self._nvim.current.buffer
        buffer[:] = lines
        self._nvim.call("oxfdictionary#add_highlight")

    def show_definition(self, arg: list) -> None:
        word = self._get_word(arg)

        if not word:
            self._error("Words are not selected.")
            return

        lines: typing.List[str] = self._check_dump(word)
        if not lines:
            response = self._get_api_msg(word)
            if response.status_code != 200:
                if response.status_code == 404:
                    self._error("No definition found")
                else:
                    self._error("Internal error")
                return
            lines = self._process_def_dict(json.loads(response.text))

        self._show_floating_window(word, copy.deepcopy(lines))
        self._update_dump(word, lines)
