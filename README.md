# OxfDictionary.nvim

A simple dictionary plugin for neovim using Oxford Dictionaries API.

## Requirements
- python3
- neovim

## Usage
Get your App ID and App KEY from [Oxford Dictionaries API](https://developer.oxforddictionaries.com/).
Then set them in your init.vim.
```vim
let g:OxfDictionary#app_id=''
let g:OxfDictionary#app_key=''
```

Execute this command with the cursor on the word you want to look up.
The word once you looked up is cached.

``` vim
:Definition
```

By taking a word as an argument, you can get the definitions of it.
```vim
:Definition [word]
```
