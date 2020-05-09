import pynvim
from .dictionary import OxfordDict

@pynvim.plugin
class Dictionary:

    def __init__(self, nvim):
        self.nvim = nvim
        self.app_id = nvim.eval("g:OxfDictionary#app_id")
        self.app_key = nvim.eval("g:OxfDictionary#app_key")

    def get_word(self,args):
        if args:
            word = args[0]
        else:
            word = self.nvim.eval('expand("<cword>")')
        return word

    def re_definition(self,word):
        if word:
            return OxfordDict(self.app_id, self.app_key).get_definition(word)
        else:
            return "Words are not selected."

    @pynvim.command('Definition', nargs='*')
    def definition(self, args=''):
        selectedW = self.get_word(args)
        self.nvim.command('echo "{}"'.format(self.re_definition(selectedW)))
