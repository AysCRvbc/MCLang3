import mclang.syntax.PrcParser as Prc
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct


class Parser(Prc.PrcParser):
    def __init__(self):
        self.name = None

    def parse(self, block, meta, base=None, data=None):
        block = block.split()
        ns: Namespace = meta["NMETA"].getNamespace()
        valtype = "dummy"
        if len(block) == 2:
            valtype = block[1]

        ns.setValue(block[0], "scoreboard", meta=valtype)
        ns.getValue(block[0])["pointer"] = self

        self.name = block[0]

    def store(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()

        command = args[0]
        res_type = "result"
        if len(args) > 1:
            res_type = args[1]
        selector = "@s"
        if len(args) > 2:
            selector = args[2]
        selector = sct.getSelector(selector, meta)

        cmd = f"execute store {res_type} score {selector} {ns.getValue(self.name)['value']} run {command}"

        return [{"type": "command", "value": cmd}]
