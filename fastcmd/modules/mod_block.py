import mclang.syntax.PrcParser as prc
import mclang.parser as pr


class Parser(prc.PrcParser):
    def getName(self):
        return "mod"

    def parse(self, block, meta, base=None, data=None):
        parser: pr.CodeParser = meta["PARSER"]
        base = block
        base = "execute " + base
        base = base.strip()
        base = base + " run "

        prc_list = parser.parse_prcs(data)
        cmds = []
        for prcl in prc_list:
            prcl['value'] = base + prcl['value']

        return prc_list