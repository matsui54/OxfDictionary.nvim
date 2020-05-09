#OxfDictionary.nvim

A simple dictionary plugin for neovim using Oxford Dictionaries API.

##Requirements
- python3

##Usage
Get your App ID and App KEY from [Oxford Dictionaries API](https://developer.oxforddictionaries.com/).
Then set them in your init.vim.
'''vim
let g:OxfDictionary#app_id=''
let g:OxfDictionary#app_key=''
'''

Execute this command with the cursor on the word you want look up.
'''vim
:Definition
'''

By taking a word as an argument, you can get the definitions of the word.
'''vim
:Definition [word...]
'''
