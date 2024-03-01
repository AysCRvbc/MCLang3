import mclang.syntax.PrcParser as prc


class Parser(prc.PrcParser):
    def getName(self):
        return "testfor"

    def parse(self, block, meta, base=None, data=None):
        return {"type": "command", "value": "say hi"}