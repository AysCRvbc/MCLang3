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
        self.n = 0
        self.nNow = 0
        self.name = None
        self.added = []
        self.parser: parser.CodeParser = None
        self.ns = None
        self.func_name = None
        self.nmeta: parser.NeccessaryMeta = None

    def parse(self, block, meta, base=None, data=None):
        prc_list = []
        func_name, args = block.split("(", 1)
        self.name = func_name
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
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

        cmds = []

        for i in prcs:
            cmds.append(i['value'])

        caller_cmds = [f'tag @s add {ns.getFunction(func_name)}']
        nmeta.addCompiled(
            {"type": "function", "data": caller_cmds, "name": ns.getFunction(func_name) + "_caller", "selector": self.selector}
        )

        self.func_name = ns.getFunction(func_name)
        nmeta.addCompiled(self.getJson(cmds))

    def getJson(self, cmds, blocked = False) -> dict:
        pre_block = cmds
        post_block = []
        block = None

        for i, cmd in enumerate(pre_block):
            if "//block" in cmd:
                block = cmd.split("//block")[1].strip()
                post_block = cmds[i + 1:]
                break

        if not post_block:
            pre_block.append(f"tag @s add {self.func_name}_ended")

        cmds = pre_block

        inserted = {}
        for i, cmd in enumerate(cmds):
            if "//block" in cmd:
                name = self.func_name
                if self.nNow > 0:
                    name += f"_{self.nNow}"
                self.nNow += 1
                ccc = f"tag @s remove {name}"
                base = cmds[i].split("//block")[0]
                cmds[i] = base + ccc
                inserted[i] = f"tag @s add {self.func_name}_waiter{self.nNow}"
                inserted[i] = base + inserted[i]

        added = 0
        for i in inserted:
            cmds.insert(i+added, inserted[i])
            added += 1

        if block:
            self.n += 1
            name = self.n
            self.nNow -= 1
            subFunc = self.getJson(post_block, blocked=True)
            subCmds = subFunc["data"]
            subFunc["name"] += f"_{name}"
            subFunc["data"] = replaceGlobalToLocalExit(self.func_name, subFunc["name"], subCmds)
            self.added.append(subFunc)

            self.added[-1]["data"].insert(0,
                f"tag @s remove {self.func_name}_waiter{name}")

            self.nmeta.addCompiled(self.added[-1])

            subfunc_name = self.added[-1]["name"].split("_", 1)[1]

            self.ns.setFunction(subfunc_name, is_global=True)
            self.ns.setFunctionField(subfunc_name, "prc", self)

            triggerBlock = [
                f"observe {self.func_name.split('_', 1)[1]}_{name} -> {self.selector}",
                f"    select tag = {self.ns.prefixy(block.split('_', 1)[1], is_global=True)}",
                f"    select tag = {self.func_name}_waiter{name}",
                f"    delete {self.ns.prefixy(block.split('_', 1)[1], is_global=True)}",
            ]
            triggerBlock = "\n".join(triggerBlock)

            self.parser.parse_code(triggerBlock)

        # if not blocked:
        #     cmds.insert(0, f"tag @s remove {self.func_name}_ended")

        return {"type": "function", "data": cmds, "name": self.func_name, "selector": self.selector}


def replaceGlobalToLocalExit(process, local, cmds):
    for i, e in enumerate(cmds):
        if e.endswith(f"tag @s remove {process}"):
            cmds[i] = e.replace(f"tag @s remove {process}", f"tag @s remove {local}")
    return cmds
