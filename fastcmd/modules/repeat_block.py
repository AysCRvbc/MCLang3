import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct
import re


def split_injections(line):
    regex = r"(%.*?%)"
    return re.split(regex, line)


class Parser(prc.PrcParser):
    def getName(self):
        return "repeat"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

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
                    e = eval(e[1:-1], {"i": i})
                line += str(e)
            code += line

        return parser.parse_prcs(code)
