import mclang.syntax.PrcParser as Prc
import mclang.utils.math_parser as mp
from mclang.namespace import Namespace

pairs = {
    ("scoreboard", "scoreboard"): "sc_sc",
    ("scoreboard", "const"): "sc_c",
    ("tag", "const"): "tag_const",
}


def recursive_array_unpack(array):
    res = []
    for el in array:
        if isinstance(el, list):
            res.extend(recursive_array_unpack(el))
        else:
            res.append(el)
    return res


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        getter, setter = [c.strip() for c in block.split("=", 1)]
        setter = mp.get_math_cmds(setter, meta)
        base = setter[2]
        retval = []

        if len(setter[0]) != 0:
            code = setter[0]
            code.append(f"{getter} = {setter[1]}")
            code = "\n".join(code)
            retval = meta["PARSER"].parse_code(code)
        else:
            retval = self.setOperation([getter, setter[1]], meta)

        base.extend(retval)
        base = recursive_array_unpack(base)

        return base

    def setOperation(self, block, meta):
        getter = block[0]
        setter = block[1]
        ns: Namespace = meta["NMETA"].getNamespace()
        if getter not in ns.variables:
            ns.setValue(getter, "scoreboard", meta="dummy")

        getter_type = ns.getType(getter)
        setter_type = ns.getType(setter)

        method = pairs[getter_type, setter_type]
        method = getattr(self, method)

        return method([getter, setter], meta)

    def sc_sc(self, variables: list, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        variables[0] = ns.getValue(variables[0])["value"]
        variables[1] = ns.getValue(variables[1])["value"]
        return [{"type": "command", "value": f"scoreboard players operation @s {variables[0]} = @s {variables[1]}"}]

    def sc_c(self, variables: list, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        variables[0] = ns.getValue(variables[0])["value"]
        setter = str(variables[1])
        if not setter.isnumeric():
            setter = ns.getValue(setter)["value"]
        return [{"type": "command", "value": f"scoreboard players set @s {variables[0]} {setter}"}]

    def tag_const(self, variables: list, meta):
        tag = variables[0].split(".", 1)[1]
        tag = meta["NMETA"].getNamespace().prefixy(tag)
        if variables[1] == "True":
            return [{"type": "command", "value": f"tag @s add {tag}"}]
        else:
            return [{"type": "command", "value": f"tag @s remove {tag}"}]