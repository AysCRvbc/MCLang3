import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace


class Parser(prc.PrcParser):
    def getName(self):
        return None
    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]