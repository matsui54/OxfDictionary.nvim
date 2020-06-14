import pynvim

from .dictionary import Dict


@pynvim.plugin
class OxfDictionary:
    def __init__(self, nvim: pynvim.Nvim):
        self._rplugin = Dict(nvim)

    @pynvim.command("Definition", nargs="*")
    def definition(self, args=[]):
        self._rplugin.show_definition(args)
