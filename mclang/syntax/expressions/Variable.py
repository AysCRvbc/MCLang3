import mclang.syntax.PrcParser as Prc
from mclang.namespace import Namespace


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        block = block.split()
        ns: Namespace = meta["NMETA"].getNamespace()
        ns.setValue(block[0], "scoreboard", meta="dummy")
        if len(block) == 2:
            ns.getValue(block[0])["objective"] = block[1]
