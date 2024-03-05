import mclang.syntax.PrcParser as Prc
import mclang.parser as parser
from mclang.namespace import Namespace


def getPath(meta_path, path, ext=""):
    path = path.replace("\\", "/")
    path = path.replace(".", "/")
    package = path.replace("/", ".")
    return meta_path + path + ext, package


class Parser(Prc.PrcParser):
    def __init__(self):
        self.bases = {
            "@name": self.nameSet,
            "@import": self.importSet,
            "@define": self.defineSet
        }

    def parse(self, *args, base=None, data=None):
        return self.bases[base](*args)

    def nameSet(self, args, meta_dict):
        meta_dict["NMETA"].setNamespace(args)

    def importSet(self, args, meta_dict):
        args, package = getPath(meta_dict['path'], args, ".mcl")

        ns: Namespace = meta_dict["NMETA"].getNamespace()
        prefix = meta_dict["NMETA"].getNamespace().prefix
        cparser = parser.CodeParser(parent=prefix)
        prc_list = cparser.get_prcs(args)
        meta_dict["NMETA"].bulk_addCompiled(prc_list)

        ns_outer: Namespace = cparser.NMeta.getNamespace()
        for key, val in ns_outer.variables.items():
            if "ignore" in val:
                if val["ignore"]:
                    continue
            key = f"{package}.{key}"
            ns.variables[key] = val
        for key, val in ns_outer.functions.items():
            if "ignore" in val:
                if val["ignore"]:
                    continue
            key = f"{package}.{key}"
            ns.functions[key] = val

    def defineSet(self, args, meta_dict):
        defType, path = args.split(" ", 1)
        match defType:
            case "block":
                module = __import__(path, fromlist=['']).Parser
                if not issubclass(module, Prc.PrcParser):
                    raise Exception(f"Module {path} must inherit PrcParser")
                name = module().getName()
                if name in parser.block_types:
                    if parser.block_types[name] == module:
                        return
                    raise Exception(f"Block {name} already exists")
                parser.block_types[name] = module
            case "expression":
                module = __import__(path, fromlist=['']).Parser
                if not issubclass(module, Prc.PrcParser):
                    raise Exception(f"Module {path} must inherit PrcParser")
                name = module().getName()
                if name in parser.line_types:
                    if parser.line_types[name] == module:
                        return
                    raise Exception(f"Line {name} already exists")
                parser.line_types[name] = module
            case _:
                raise Exception(f"Unknown definition type: {defType}")


