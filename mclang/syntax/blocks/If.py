import mclang.syntax.PrcParser as Prc
import mclang.syntax.expressions.lang.VariableSet as vs
import mclang.parser as pr
from mclang.namespace import Namespace


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]
        ns.setValue("temp", "scoreboard")
        code = f"temp = {block}"
        prs_code = vs.Parser().parse(code, meta)

        base = f"execute if score @s {ns.getValue('temp')['value']} matches 1 run "
        prc_list2 = parser.parse_prcs(data)
        cmds = []
        for prc in prc_list2:
            prc['value'] = base + prc['value']
            cmds.append(prc)
        prs_code += cmds

        return prs_code
