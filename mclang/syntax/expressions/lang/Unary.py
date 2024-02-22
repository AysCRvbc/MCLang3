import re
import mclang.syntax.PrcParser as Prc
from mclang import parser
from mclang.namespace import Namespace


def getNumName(operation):
    operations_mapping = {"+": "plus", "-": "sub", "*": "mul", "/": "div", "%": "mod",
                          ">": "gt", "<": "lt", ">~": "gte", "<~": "lte", "~": "eq"}

    sub_name = operations_mapping.get(operation)
    if sub_name is None:
        raise SyntaxError(f"Operation {operation} is not supported YET")

    return f"{sub_name}_srvc"


def parse_string(input_string):
    pattern = re.compile(r'(?P<arg1>\b\w+(?:\.\w+)*)\s*(?P<operator>\+|-|/|\*|%|>|<|>~|<~|~)=\s*(?P<arg2>\b\w+(?:\.\w+)*|\d+)\b')

    match = pattern.match(input_string)

    if match:
        varname_1 = match.group(1)
        operation = match.group(2)
        varname_2 = match.group(3)

        return True, varname_1, operation, varname_2
    else:
        return False, None, None, None


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        res = []
        ns: Namespace = meta["NMETA"].getNamespace()
        parsed = parse_string(block)
        if not parsed[0]:
            print(block)
            raise Exception("Incorrect format")
        getter = parsed[1]
        operation = parsed[2]
        setter: str = parsed[3]

        if setter.isnumeric():
            sub_name = getNumName(operation)
            res.append(f"{sub_name} = {setter}")
            setter = ns.setValue(sub_name, "scoreboard")['value']
        else:
            setter = ns.getValue(setter)["value"]

        getter = ns.getValue(getter)["value"]

        comparatives = [">", "<", "~", ">~", "<~"]
        if operation in comparatives:
            replace_dict = {"~": "=",
                            ">~": ">=",
                            "<~": "<="}
            if operation in replace_dict:
                operation = replace_dict[operation]
            res.append(f"execute execute if score @s {getter} {operation} @s {setter} run scoreboard set @s {getter} 1")
            res.append(f"execute execute unless score @s {getter} {operation} @s {setter} run scoreboard set @s {getter} 0")
        else:
            res.append(f"execute scoreboard players operation @s {getter} {operation}= @s {setter}")

        prs: parser.CodeParser = meta["PARSER"]
        code = "\n".join(res)

        res = prs.parse_code(code)
        return res
