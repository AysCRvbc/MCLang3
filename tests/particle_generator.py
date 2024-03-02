import mclang.syntax.PrcParser as prc


class Parser(prc.PrcParser):
    def getName(self):
        return "image"

    def parse(self, block, meta, base=None, data=None):
        raise NotImplementedError()