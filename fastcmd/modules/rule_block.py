import mclang.syntax.PrcParser as prc
import mclang.syntax.expressions.Selector as sct
import mclang.parser as pr
from mclang.namespace import Namespace


class Parser(prc.PrcParser):
    def getName(self):
        return "rule"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]
        name, args = block.split("(", 1)
        args = sct.parse_arguments(args)
        args = [arg for arg in args if arg if arg]

        selector = "@e"
        if len(block.split("->")) > 1:
            selector = block.split("->")[1].strip()
            selector = sct.getSelector(selector, meta)

        for i, e in enumerate(args):
            args[i] = ns.prefixy(e, is_global=True)

        code = f"""func {name}() -> {selector}\n"""
        for line in data.splitlines():
            code += f"    {line}\n"

        code+= f"""observe {name} -> {selector}\n"""
        for arg in args:
            code += f"    select tag = {arg}"
        if len(args) == 0:
            code += f"    pass"

        prcs = parser.parse_code(code)