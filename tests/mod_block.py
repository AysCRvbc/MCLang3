import mclang.syntax.PrcParser as prc


class Parser(prc.PrcParser):
    def getName(self):
        return "mod"

    def parse(self, block, meta, base=None, data=None):
        raise NotImplementedError()

    def show(self, args: list, meta):
        raise NotImplementedError()