import mclang.syntax.PrcParser as Prc
import mclang.parser as parser
from mclang.namespace import Namespace


#аааааа, ужас!

def parse_arguments(raw_arguments):
    arguments = []
    current_argument = ""
    in_quotes = False
    nesting_level = 0


    for char in raw_arguments:
        if nesting_level == 0 and char == ")":
            break
        if char == "," and nesting_level == 0 and not in_quotes:
            arguments.append(current_argument.strip())
            current_argument = ""
        elif char == "'" or char == '"':
            current_argument += char
            in_quotes = not in_quotes
        elif char == "(" or char == "[":
            current_argument += char
            nesting_level += 1
        elif char == ")" or char == "]":
            current_argument += char
            nesting_level -= 1
        else:
            current_argument += char

    arguments.append(current_argument.strip())

    return arguments


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        func_name, args = block.split("(", 1)
        nmeta: parser.NeccessaryMeta = meta["NMETA"]

        ns: Namespace = meta["NMETA"].getNamespace()
        old_ns = ns

        args = parse_arguments(args)
        for i in args:
            ns.setValue(i, "scoreboard")




        prs: parser.CodeParser = meta["PARSER"]
        prs.meta = meta.copy()
        prs.meta["NMETA"].setNamespace(func_name)
        prcs = prs.parse_prcs(data)
        prs.meta["NMETA"].namespace = ns
