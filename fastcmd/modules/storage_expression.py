import mclang.syntax.PrcParser as prc
from mclang import parser as pr
from mclang.namespace import Namespace


class Parser(prc.PrcParser):
    def __init__(self):
        self.type = None
        self.name = None
        self.code = ""

    def getName(self):
        return "storage"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = nmeta.getNamespace()

        self.type, self.name = block.split(" ", 2)

        ns.setValue(self.name, "storage")
        ns.getValue(self.name)['pointer'] = self

    def put(self, args, meta):
        nmeta = meta["NMETA"]
        parser: pr.CodeParser = meta["PARSER"]
        ns: Namespace = nmeta.getNamespace()

        var = args[0]
        var_ns = ns.getValue(var)
        if var_ns['type'] != "scoreboard" and var_ns['type'] != "float":
            raise Exception("Only scoreboard and float can be used as storage")

        var_path = var_ns['value']
        main_path = ns.global_name
        mypath = ns.getValue(self.name)['value'].split(main_path + "_", 1)[1]
        code = f"execute execute store result storage {main_path} {mypath} {self.type} 1 run scoreboard players get @s {var_path}"
        return parser.parse_prcs(code)

    def pull(self, args, meta):
        nmeta = meta["NMETA"]
        parser: pr.CodeParser = meta["PARSER"]
        ns: Namespace = nmeta.getNamespace()

        var = args[0]
        try:
            mul = float(args[1])
        except:
            mul = 1

        var_ns = ns.getValue(var)
        if var_ns['type'] != "scoreboard" and var_ns['type'] != "float":
            raise Exception("Only scoreboard and float can be used as storage")

        var_path = var_ns['value']
        main_path = ns.global_name
        mypath = ns.getValue(self.name)['value'].split(main_path + "_", 1)[1]

        code = f"execute execute store result score @s {var_path} run data get storage minecraft:{main_path} {mypath} {mul}"
        return parser.parse_prcs(code)