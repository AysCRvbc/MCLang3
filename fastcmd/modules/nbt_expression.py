import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace


class Parser(prc.PrcParser):
    def __init__(self):
        self.name = None

    def getName(self):
        return "nbt"
    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        self.name, value = block.split("=", 1)
        self.name = self.name.strip()
        value = value.strip()

        ns.setValue(self.name, "nbt")
        ns.getValue(self.name)['pointer'] = self
        ns.getValue(self.name)['nbt'] = value

    def storeFloat(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        cmd = (f"execute store result entity @s {ns.getValue(self.name)['nbt']} float 0.01 run "
               f"scoreboard players get @s {ns.getValue(args[0])['value']}")

        return {"type": "command", "value": cmd}

    def storeInt(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        cmd = (f"execute store result entity @s {ns.getValue(self.name)['nbt']} int 1 run "
               f"scoreboard players get @s {ns.getValue(args[0])['value']}")

        return {"type": "command", "value": cmd}

    def storeDouble(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]
        mult = 1
        if len(args) == 0:
            raise ValueError("need an argument")
        if len(args) == 2:
            mult = args[1]


        cmd = (f"execute store result entity @s {ns.getValue(self.name)['nbt']} double {mult} run "
               f"scoreboard players get @s {ns.getValue(args[0])['value']}")

        return {"type": "command", "value": cmd}
