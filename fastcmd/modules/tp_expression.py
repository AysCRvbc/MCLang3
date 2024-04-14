import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct


class Parser(prc.PrcParser):
    def getName(self):
        return "tp"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        target, place = sct.parse_arguments(block)
        target_sct = sct.getSelector(target, meta)
        place_sct = sct.getSelector(place, meta)

        code = f"execute tp {target_sct} {place_sct}"
        return parser.parse_prcs(code)
