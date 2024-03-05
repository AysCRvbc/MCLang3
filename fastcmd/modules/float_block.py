import mclang.syntax.PrcParser as prc
import mclang.parser as pr
import mclang.syntax.expressions.Selector as sct
import mclang.syntax.expressions.lang.VariableSet as vs
import mclang.namespace as nss
from mclang.namespace import Namespace


atan_code = f"""float sign
float res
float temp_atan
sign.set(1)
if %val% > 0
    sign.set(-1)
%val%.antiabs()

if %val% < -362
    %val%.set(-1.4)
else
    %val%.add(2)
    
    res.set(-1.1)
    temp_atan.set(%val%)
    temp_atan.mul(0.2)
    res.add(temp_atan)
    
    temp_atan.set(%val%)
    temp_atan.pow(2)
    temp_atan.mul(0.08)
    res.add(temp_atan)
    
    temp_atan.set(%val%)
    temp_atan.pow(3)
    temp_atan.mul(0.03)
    res.add(temp_atan)
    
    temp_atan.set(%val%)
    temp_atan.pow(4)
    temp_atan.mul(0.01)
    res.add(temp_atan)
    
    res.mul(sign)
    %val%.set(res)
"""

antiabs_code = f"""if %val% > 0
    %val% *= -1
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
            val = int(float(val)*100)
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
            val = int(round(float(val)*100))

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
            val = int(float(val)*100)
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

    def mul(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(float(val)*100)
        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        code = (f"{self.name} *= {val}\n"
                f"{self.name} /= 100")

        return parser.parse_prcs(code)

    def add(self, args, meta):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        val = args[0]
        try:
            val = int(float(val)*100)
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
            val = int(float(val)*100)
        except:
            if ns.getValue(val)['type'] != "float":
                raise Exception("float expected")

        frac_val = val//100

        frac_val = 100**frac_val

        setter = f"{self.name}"
        while val > 100:
            setter += f" * {self.name}"
            val -= 100

        prcs = parser.parse_prcs(f"{self.name} = {setter}")

        prcs.extend(
            parser.parse_prcs(f"{self.name} /= {frac_val}"))

        return prcs