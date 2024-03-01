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


def getComment(line):
    comment_start = line.find('#')
    if comment_start == -1:
        return ''

    in_string = False
    c_n = 0
    for c in line:
        if c == '"':
            if in_string:
                return getComment(line[c_n + 1:])
            in_string = not in_string
        elif c == "#":
            if not in_string:
                return line[c_n:]
        c_n += 1


class Parser(Prc.PrcParser):
    def __init__(self, ns: Namespace = None):
        self.selector = None
        self.ns = ns
        self.name = None
        self.added = []
        self.parser: parser.CodeParser = None
        self.ns = None
        self.func_name = None
        self.nmeta: parser.NeccessaryMeta = None
        self.nBlock = 0
        self.n = 0

    def parse(self, block, meta, base=None, data=None):
        prc_list = []
        func_name, args = block.split("(", 1)
        self.name = func_name
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
        oldCurFunc = nmeta.getCurFunc()
        nmeta.setCurFunc(self)
        prs: parser.CodeParser = meta["PARSER"]
        nmeta.setProcess(func_name)

        self.nmeta = nmeta

        self.parser = prs

        self.selector = block.split("->", 1)
        if len(self.selector) == 1:
            self.selector = "@e"
        else:
            self.selector = self.selector[1].strip()
            self.selector = sct.getSelector(self.selector, meta)

        ns: Namespace = self.ns
        if self.ns is None:
            ns = nmeta.getNamespace()
        old_ns = ns

        ns.setFunction(func_name)
        ns.setFunctionField(func_name, "prc", self)

        args = parse_arguments(args)
        args = [arg for arg in args if arg]
        for n, i in enumerate(args):
            prc_list.append(f"{i} = arg{n}")
            ns.setValue(f"arg{n}", "scoreboard", meta="dummy")

        prs.meta = meta.copy()
        if self.ns is None:
            nmeta.setNamespace(func_name)
        self.ns = nmeta.getNamespace()
        prcs = prs.parse_prcs("\n".join(prc_list) + "\n" + data)
        nmeta.namespace = old_ns
        nmeta.setCurFunc(oldCurFunc)

        cmds = []

        for i in prcs:
            cmds.append(i['value'])

        caller_cmds = [f'tag @s add {ns.getFunction(func_name)}']
        nmeta.addCompiled(
            {"type": "function", "data": caller_cmds, "name": ns.getFunction(func_name) + "_caller",
             "selector": self.selector}
        )

        self.func_name = ns.getFunction(func_name)
        cmds = self.preHandling(cmds, self.func_name)
        nmeta.addCompiled(self.getJson(cmds))

    def newBlock(self):
        self.nBlock += 1

    def preHandling(self, cmds, waiter_name):
        for i, e in enumerate(cmds):
            e = getComment(e)
            if e.startswith("#block"):
                base = cmds[i].split(e)[0]
                block = e.split("#block")[1].strip()
                waiter, blocker = block.split(" ", 1)
                waiter = f"{waiter_name}_waiter{waiter}"
                cmds[i] = [
                    f"{base}tag @s add {waiter}",
                    f"{base}tag @s remove {self.func_name}",
                    f"{base}#block {waiter} {blocker}"
                ]
        cmds = parser.recursive_array_unpack(cmds)
        return cmds

    def getJson(self, cmds, blocked=False) -> dict:
        post_block = []
        block = None

        for i, e in enumerate(cmds):
            if getComment(e):
                post_block = cmds[i + 1:]
                block = getComment(e)
                break

        if block:
            self.n += 1
            block = block.split(" ", 1)[1]
            waiter, block = block.split(" ", 1)
            subfunc_name = f"{self.func_name.split('_', 1)[1]}_{self.n}"
            self.ns.setFunction(subfunc_name, is_global=True)
            self.ns.setFunctionField(subfunc_name, "prc", self)

            subFunc = self.getJson(post_block, blocked=True)
            subCmds = subFunc["data"]
            subFunc["name"] = self.ns.getFunction(subfunc_name)
            subFunc["data"] = replaceGlobalToLocalExit(self.func_name, subFunc["name"], subCmds)
            subFunc["data"].insert(0,
                                   f"tag @s remove {waiter}")
            self.nmeta.addCompiled(subFunc)

            triggerBlock = [
                f"observe {subfunc_name} -> {self.selector}",
                f"    select tag = {block}",
                f"    select tag = {waiter}",
                f"    delete {block}",
            ]

            triggerBlock = "\n".join(triggerBlock)

            self.parser.parse_code(triggerBlock)
        else:
            cmds.append(f"tag @s add {self.func_name}_ended")

        cmds_block_deleted = []
        for i in cmds:
            if not getComment(i):
                cmds_block_deleted.append(i)

        return {"type": "function", "data": cmds_block_deleted, "name": self.func_name, "selector": self.selector}


def replaceGlobalToLocalExit(process, local, cmds):
    for i, e in enumerate(cmds):
        if e.endswith(f"tag @s remove {process}"):
            cmds[i] = e.replace(f"tag @s remove {process}", f"tag @s remove {local}")
    return cmds
