import mclang.syntax.PrcParser as Prc


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        return [{"type": "command", "value": block}]
