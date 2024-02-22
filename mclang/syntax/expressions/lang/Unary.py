import re
import mclang.syntax.PrcParser as Prc
from mclang import parser
from mclang.namespace import Namespace


def getNumName(operation):
    if operation == "+":
        sub_name = "plus_srvc"
    elif operation == "-":
        sub_name = "sub_srvc"
    elif operation == "*":
        sub_name = "mul_srvc"
    elif operation == "/":
        sub_name = "div_srvc"
    elif operation == "%":
        sub_name = "mod_srvc"
    elif operation == ">":
        sub_name = "gt_srvc"
    elif operation == "<":
        sub_name = "lt_srvc"
    elif operation == ">~":
        sub_name = "gte_srvc"
    elif operation == "<~":
        sub_name = "lte_srvc"
    elif operation == "~":
        sub_name = "eq_srvc"
    else:
        raise SyntaxError(f"Operation {operation} is not supported YET")

    return sub_name


def parse_string(input_string):
    pattern = re.compile(r'^\s*(\w+)\s*([+\-*/%><~]{1,})=\s*(\w+)\s*$')

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
            res.append(f"execute execute unless score @s {getter} {operation} @s {setter} run scoreboard set @s {getter} 1")
        else:
            res.append(f"execute scoreboard players operation @s {getter} {operation}= @s {setter}")

        prs: parser.CodeParser = meta["PARSER"]
        code = "\n".join(res)

        res = prs.parse_code(code)
        return res
