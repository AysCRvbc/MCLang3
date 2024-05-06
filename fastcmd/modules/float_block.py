import mclang.syntax.PrcParser as prc
import mclang.parser as pr
import mclang.syntax.expressions.Selector as sct
import mclang.syntax.expressions.lang.VariableSet as vs
import mclang.namespace as nss
from mclang.namespace import Namespace

atan_code = f"""float sign_atan_func
float res_atan_func
float temp_atan_func
sign_atan_func.set(1)
if %val% > 0
    sign_atan_func.set(-1)
%val%.antiabs()

if %val% < -362
    %val%.set(-1.4)
else
    %val%.add(2)
    
    res_atan_func.set(-1.1)
    temp_atan_func.set(%val%)
    temp_atan_func.mul(0.2)
    res_atan_func.add(temp_atan_func)
    
    temp_atan_func.set(%val%)
    temp_atan_func.pow(2)
    temp_atan_func.mul(0.08)
    res_atan_func.add(temp_atan_func)
    
    temp_atan_func.set(%val%)
    temp_atan_func.pow(3)
    temp_atan_func.mul(0.03)
    res_atan_func.add(temp_atan_func)
    
    temp_atan_func.set(%val%)
    temp_atan_func.pow(4)
    temp_atan_func.mul(0.01)
    res_atan_func.add(temp_atan_func)
    
    res_atan_func.mul(sign_atan_func)
    %val%.set(res_atan_func)
"""

antiabs_code = f"""if %val% > 0
    %val% *= -1
"""

round_code = f"""float res_round_func
res_round_func.set(%val%)
res_round_func %= 100
if res_round_func >= 50
    %val% /= 100
    %val% += 1
    %val% *= 100
else
    %val% /= 100
    %val% *= 100
"""

relu_code = f"""if %val% < 0
    %val%.set(0)
"""

pi2_cycle_approx_code = f"""
float temp_pi2_cycle_approx
float temp_pi2_cycle_approx_pi2
float temp2_pi2_cycle_approx
temp_pi2_cycle_approx.set(%val%)
temp_pi2_cycle_approx_pi2.set(6.28)
temp_pi2_cycle_approx.frac(temp_pi2_cycle_approx_pi2)
temp_pi2_cycle_approx.round()
temp_pi2_cycle_approx.mul(temp_pi2_cycle_approx_pi2)
temp2_pi2_cycle_approx.set(%val%)
temp2_pi2_cycle_approx.sub(temp_pi2_cycle_approx)
%val% = temp2_pi2_cycle_approx
"""

sin_code = f"""
%val%.pi2_cycle_approx()
float temp_sin_func_res
float temp_sin_func_temp
float temp_sin_func_temp1
float temp_sin_func_temp2
float temp_sin_func_temp3
temp_sin_func_temp1.set(%val%)
temp_sin_func_temp2.set(%val%)
temp_sin_func_temp3.set(%val%)
temp_sin_func_temp1.frac(12)
temp_sin_func_temp2.pow(3)
temp_sin_func_temp2.frac(569)
temp_sin_func_temp1.sub(temp_sin_func_temp2)
temp_sin_func_temp3.pow(2)
temp_sin_func_temp3.frac(10)
temp_sin_func_temp3.mul(temp_sin_func_temp1)
temp_sin_func_temp1.set(%val%)
temp_sin_func_temp2.set(temp_sin_func_temp3)
temp_sin_func_temp3.set(%val%)
temp_sin_func_temp1.frac(6)
temp_sin_func_temp1.sub(temp_sin_func_temp2)
temp_sin_func_temp3.mul(temp_sin_func_temp1)
temp_sin_func_temp1.set(1)
temp_sin_func_temp2.set(temp_sin_func_temp3)
temp_sin_func_temp3.set(%val%)
temp_sin_func_temp1.sub(temp_sin_func_temp2)
temp_sin_func_temp3.mul(temp_sin_func_temp1)
%val% = temp_sin_func_temp3
"""

cos_code = f"""
%val%.add(1.57)
%val%.sin()
"""


def float_float(self, variables: list, meta):
    ns: Namespace = meta["NMETA"].getNamespace()
    variables[0] = ns.getValue(variables[0])["value"]
    variables[1] = ns.getValue(variables[1])["value"]
    res = [{"type": "command", "value": f"scoreboard players operation @s {variables[0]} = @s {variables[1]}"}]
    return res


def float_const(self, variables: list, meta):
    ns: Namespace = meta["NMETA"].getNamespace()
    variables[0] = ns.getValue(variables[0])["value"]
    setter = str(variables[1])
    if not setter.isnumeric():
        setter = ns.getValue(setter)["value"]
    return [{"type": "command", "value": f"scoreboard players set @s {variables[0]} {setter}"}]


def sc_float(self, variables: list, meta):
    ns: Namespace = meta["NMETA"].getNamespace()
    variables[0] = ns.getValue(variables[0])["value"]
    variables[1] = ns.getValue(variables[1])["value"]
    res = [{"type": "command", "value": f"scoreboard players operation @s {variables[0]} = @s {variables[1]}"}]
    return res


def float_sc(self, variables: list, meta):
    ns: Namespace = meta["NMETA"].getNamespace()
    variables[0] = ns.getValue(variables[0])["value"]
    variables[1] = ns.getValue(variables[1])["value"]
    res = [{"type": "command", "value": f"scoreboard players operation @s {variables[0]} = @s {variables[1]}"}]
    return res


class Parser(prc.PrcParser):
    def __init__(self):
        self.name = None
        vs.pairs["float", "float"] = "float_float"
        vs.pairs["float", "const"] = "float_const"
        vs.pairs["scoreboard", "float"] = "sc_float"
        vs.pairs["float", "scoreboard"] = "float_sc"
        vs.Parser.float_float = float_float
        vs.Parser.float_const = float_const
        vs.Parser.sc_float = sc_float
        vs.Parser.float_sc = float_sc

    def getName(self):
        return "float"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()

        ns.setValue(block, "float", )
        ns.getValue(block)['objectives'] = "dummy"
        ns.getValue(block)['pointer'] = self
        self.name = block
        nss.scoreboard_variables.append(ns.getValue(block))

    def setFromNbt(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        nbt_path = args[0]
        if nbt_path in ns.variables:
            nbt_path = ns.getValue(nbt_path)['nbt']
        selector = "@s"
        if len(args) > 1:
            selector = args[1]
        selector = sct.getSelector(selector, meta)
        cmd = (f"execute as @s store result score @s {ns.getValue(self.name)['value']} "
               f"run data get entity {selector} {nbt_path} 100")

        return {"type": "command", "value": cmd}

    def sub(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(float(val) * 100)
        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        code = f"{self.name} -= {val}"
        return parser.parse_prcs(code)

    def set(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(round(float(val) * 100))

        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        code = f"{self.name} = {val}"
        return parser.parse_prcs(code)

    def frac(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(float(val) * 100)
        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        code = f"{self.name} *= 100"
        prc_list = parser.parse_prcs(code)

        prc_list.extend(
            parser.parse_prcs(f"{self.name} /= {val}")
        )

        return prc_list

    def atan(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        code = atan_code.replace("%val%", self.name)
        prcs = parser.parse_prcs(code)
        return prcs

    def antiabs(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        code = antiabs_code.replace("%val%", self.name)
        prcs = parser.parse_prcs(code)
        return prcs

    def round(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        code = round_code.replace("%val%", self.name)
        prcs = parser.parse_prcs(code)
        return prcs

    def pi2_cycle_approx(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        code = pi2_cycle_approx_code.replace("%val%", self.name)
        prcs = parser.parse_prcs(code)
        return prcs

    def sin(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        code = sin_code.replace("%val%", self.name)
        prcs = parser.parse_prcs(code)
        return prcs

    def cos(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        code = cos_code.replace("%val%", self.name)
        prcs = parser.parse_prcs(code)
        return prcs

    def mul(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(float(val) * 100)
        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        code = (f"{self.name} *= {val}\n"
                f"{self.name} /= 100")

        return parser.parse_prcs(code)

    def multiplied(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        setter = args[0]
        val = args[1]
        try:
            val = int(float(val))
        except:
            raise Exception("float expected in second argument")

        code = (f"{self.name} *= {val}\n"
                f"{self.name} /= 100")

        return parser.parse_prcs(code)

    def add(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(float(val) * 100)
        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        code = f"{self.name} += {val}"
        return parser.parse_prcs(code)

    def pow(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(float(val) * 100)
        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        frac_val = val // 100 - 1

        frac_val = 100 ** frac_val

        setter = f"{self.name}"
        while val > 100:
            setter += f" * {self.name}"
            val -= 100

        prcs = parser.parse_prcs(f"{self.name} = {setter}")

        prcs.extend(
            parser.parse_prcs(f"{self.name} /= {frac_val}"))

        return prcs

    def linear(self, args, meta):
        pass

    def relu(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        code = relu_code.replace("%val%", self.name)
        prcs = parser.parse_prcs(code)
        return prcs
