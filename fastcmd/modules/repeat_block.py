import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct
import re


def split_injections(line):
    regex = r"(%.*?%)"
    return re.split(regex, line)


eval_namespace = {}


class Parser(prc.PrcParser):
    def getName(self):
        return "repeat"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        prcs = []
        if block.split(" ", 1)[0] == "for":
            prcs = self.parse_for(block, data, parser)
        else:
            prcs = self.parse_range(block, data, parser)

        return prcs

    def parse_for(self, block, data, parser):
        ev_ns = eval_namespace
        code = ""
        splitted = split_injections(data)
        block_var = block.split(" ")[1]
        code_eval = f"{block}:"
        code_eval_inner = f"""\nline = \"\"
for e in splitted:
    if e[0] == \"%\" and e[-1] == \"%\":
        ev_ns[\"{block_var}\"] = {block_var}
        try:
            e = eval(e[1:-1], ev_ns.copy())
        except:
            pass
    line += str(e)
code += line
"""
        code_eval_inner = "\n    ".join(code_eval_inner.splitlines())
        code_eval += code_eval_inner
        lmao = locals().copy()
        exec(code_eval, lmao)
        code = lmao["code"]

        prcs = parser.parse_prcs(code)
        eval_namespace.pop(block_var)
        return prcs

    def parse_range(self, block, data, parser):
        block_name, args = block.split("(", 1)
        args = sct.parse_arguments(args)
        try:
            args = [int(e) for e in args]
        except ValueError:
            raise Exception("Invalid arguments. All arguments must be numbers.")
        range_repeat = range(*args)

        code = ""
        splitted = split_injections(data)
        for i in range_repeat:
            line = ""
            for e in splitted:
                if e[0] == "%" and e[-1] == "%":
                    eval_namespace[block_name] = i
                    e = eval(e[1:-1], eval_namespace.copy())
                line += str(e)
            code += line

        prcs = parser.parse_prcs(code)
        eval_namespace.pop(block_name)
        return prcs
