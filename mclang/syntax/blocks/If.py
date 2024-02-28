import mclang.syntax.PrcParser as Prc
import mclang.syntax.expressions.lang.VariableSet as vs
import mclang.parser as pr
from mclang.namespace import Namespace


class Parser(Prc.PrcParser):
    def __init__(self):
        self.cond = None

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]
        tempvar = f"ifvar{nmeta.level}_{nmeta.index}"
        ns.setValue(tempvar, "scoreboard", meta="dummy")
        code = f"{tempvar} = {block}"
        prs_code = vs.Parser().parse(code, meta)

        self.cond = f"score @s {ns.getValue(tempvar)['value']}"
        base = f"execute if {self.cond} matches 1 run "

        prc_list2 = parser.parse_prcs(data)
        cmds = []
        for prc in prc_list2:
            prc['value'] = base + prc['value']
            cmds.append(prc)
        prs_code += cmds

        return prs_code
