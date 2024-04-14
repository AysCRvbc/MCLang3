import mclang.syntax.PrcParser as Prc
from mclang.namespace import Namespace


def parse_arguments(raw_arguments):
    arguments = []
    current_argument = ""
    in_quotes = False
    nesting_level = 0
    for char in raw_arguments:
        if nesting_level == 0 and (char == ")" or char == "]"):
            break
        elif char == "," and nesting_level == 0 and not in_quotes:
            arguments.append(current_argument.strip())
            current_argument = ""
        elif char == " " and (not in_quotes):
            pass
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


def getSelector(name: str, meta):
    ns = meta["NMETA"].getNamespace()
    f_sq = name.find("[")
    if f_sq == -1:
        return ns.getValue(name)['value']

    base = name[:f_sq]
    mods = name[f_sq + 1:-1]
    base_selector = ns.getValue(base)['value']
    base_mods = parse_arguments(mods)
    base = base_selector
    f_sq = base_selector.find("[")
    if f_sq != -1:
        mods_start = base_selector[f_sq + 1:-1]
        start_mods = parse_arguments(mods_start)
        base_mods.extend(start_mods)
        base = base_selector[:f_sq]

    mods = f"[{','.join(base_mods)}]"
    if mods == "[]":
        mods = ""

    return f"{base}{mods}"


class Parser(Prc.PrcParser):
    def __init__(self):
        self.name = None

    def parse(self, block, meta, base=None, data=None):
        getter, setter = [c.strip() for c in block.split("=", 1)]
        self.name = getter
        ns: Namespace = meta["NMETA"].getNamespace()
        ns.setValue(getter, "selector")
        ns.variables[getter]["value"] = setter
        ns.getValue(getter)["pointer"] = self

    def get_value(self, ns):
        return ns.getValue(self.name)['value']

    def addTag(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        if len(args) > 1:
            raise Exception("Too many arguments. Only one argument is allowed.")

        data = ns.prefixy(args[0], is_global=True)
        add = f"[tag={data}]"
        new_selector = getSelector(self.name + add, meta)
        ns.getValue(self.name)['value'] = new_selector
