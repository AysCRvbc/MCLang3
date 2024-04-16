import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct


class Parser(prc.PrcParser):
    def getName(self):
        return "store"
    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        prcs = parser.parse_prcs(data)
        store_type, store_var = block.split(" to ", 1)
        store_var = ns.getValue(store_var)['value']
        base_cmd = f"execute store {store_type} score @s {store_var} run "
        for prc in prcs:
            prc['value'] = base_cmd + prc['value']

        return prcs
