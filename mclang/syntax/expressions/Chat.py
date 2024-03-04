import mclang.syntax.PrcParser as Prc
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct


def split_array_to_json(array_string):
    array_string = array_string[1:-1]
    res = []
    res_2 = []

    is_string = False

    for i in range(len(array_string)):
        if array_string[i] == '"':
            is_string = not is_string
        elif array_string[i] == ',' and not is_string:
            res.append(i)

    res.insert(0, 0)
    res.append(len(array_string))

    for i in range(len(res) - 1):
        subs = array_string[res[i]:res[i + 1]]
        if i > 0:
            subs = subs[2:]
        res_2.append(subs)

    return res_2


def string_check(s):
    s = s.replace('"', "'")
    if s[0] == "'" and s[-1] == "'":
        return True
    return False


class Parser(Prc.PrcParser):
    def __init__(self):
        self.nmeta = None
        self.base = None

    def replaceValue(self, s):
        ns: Namespace = self.nmeta.getNamespace()
        if string_check(s):
            return s
        else:
            return ns.getValue(s)
    def parse(self, block, meta, base=None, data=None):
        ns: Namespace = meta["NMETA"].getNamespace()
        self.nmeta = meta["NMETA"]
        name, arg = [o.strip() for o in block.split("=", 1)]

        base = split_array_to_json(arg)
        self.base = []
        for val in base:
            self.base.append(self.replaceValue(val))

        ns.setValue(name, "chat")
        ns.getValue(name)["pointer"] = self

    def log(self, args: list, meta):
        selector = sct.getSelector(args[0], meta)
        msg = args[1]
        msg = split_array_to_json(msg)


        msgs = self.base.copy()
        for m in msg:
            msgs.append(self.replaceValue(m))
            if not (isinstance(msgs[-1], str)):
                msgs[-1] = msgs[-1]['value']

        res = []
        for m in msgs:
            if string_check(m):
                res.append({"text": m[1:-1]})
            else:
                res.append({"score": {"name": "@s", "objective": m}})
        arg = str(res).replace("'", '"')

        cmd = f"tellraw {selector} {arg}"
        res = {"type": "command", "value": cmd}

        return [res]
