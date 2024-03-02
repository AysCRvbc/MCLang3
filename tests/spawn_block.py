import mclang.syntax.PrcParser as prc


class Parser(prc.PrcParser):
    def getName(self):
        return "spawn"

    def parse(self, block, meta, base=None, data=None):
        raise NotImplementedError()