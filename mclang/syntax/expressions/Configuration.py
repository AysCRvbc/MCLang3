import mclang.syntax.PrcParser as Prc
import mclang.parser as parser
from mclang.namespace import Namespace


class Parser(Prc.PrcParser):
    def __init__(self):
        self.bases = {
            "@name": self.nameSet,
            "@import": self.importSet
        }

    def parse(self, *args, base=None):
        return self.bases[base](*args)

    def nameSet(self, args, meta_dict):
        meta_dict["NMETA"].setNamespace(args)

    def importSet(self, args, meta_dict):
        args = args.replace("\\", "/")
        args = args.replace(".", "/")
        package = args.replace("/", ".")
        ns: Namespace = meta_dict["NMETA"].getNamespace()
        prefix = meta_dict["NMETA"].getNamespace().prefix
        args += ".mcl"
        args = meta_dict['path'] + args
        cparser = parser.CodeParser(parent=prefix)
        prc_list = cparser.get_prc_node(args)
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

