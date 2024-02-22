import mclang.syntax.PrcParser as Prc
import mclang.parser as parser
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct


# аааааа, ужас!

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
    def __init__(self, ns: Namespace = None):
        self.selector = None
        self.ns = ns

    def parse(self, block, meta, base=None, data=None):
        prc_list = []
        func_name, args = block.split("(", 1)
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
        prs: parser.CodeParser = meta["PARSER"]
        nmeta.setProcess(func_name)

        self.selector = block.split("->", 1)
        if len(self.selector) == 1:
            self.selector = "@e"
        else:
            self.selector = self.selector[1].strip()
            self.selector = sct.getSelector(self.selector, meta)

        ns: Namespace = self.ns
        if self.ns is None:
            ns = nmeta.getNamespace()
            ns.setFunction(func_name)
            ns.setFunctionField(func_name, "prc", self)
        old_ns = ns

        args = parse_arguments(args)
        args = [arg for arg in args if arg]
        for n, i in enumerate(args):
            prc_list.append(f"{i} = arg{n}")
            ns.setValue(f"arg{n}", "scoreboard")

        prs.meta = meta.copy()
        if self.ns is None:
            nmeta.setNamespace(func_name)
        prcs = prs.parse_prcs("\n".join(prc_list) + "\n" + data)
        nmeta.namespace = old_ns
        self.ns = ns

        cmds = []

        for i in prcs:
            cmds.append(i['value'])

        cmds.append(f"execute tag @s remove {ns.getFunction(func_name)}")

        nmeta.addCompiled(
            {"type": "function", "data": cmds, "name": ns.getFunction(func_name), "selector": self.selector})
