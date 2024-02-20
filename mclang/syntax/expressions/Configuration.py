import mclang.syntax.PrcParser as Prc
import mclang.parser as parser


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
        prefix = meta_dict["NMETA"].getNamespace().prefix
        args += ".mcl"
        args = meta_dict['path'] + args
        cparser = parser.CodeParser(parent=prefix)
        prc_list = cparser.get_prc_node(args)
        meta_dict["NMETA"].bulk_addCompiled(prc_list)
