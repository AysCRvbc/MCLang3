import mclang.syntax.PrcParser as Prc

import mclang.parser as pr

import mclang.syntax.blocks.If as If


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        parser: pr.CodeParser = meta["PARSER"]
        nmeta: pr.NeccessaryMeta = meta["NMETA"]
        prevb = nmeta.prevBlock
        if not isinstance(prevb, If.Parser):
            raise Exception("else block must be in if block")

        base = f"execute unless {prevb.cond}"

        prc_list2 = parser.parse_prcs(data)
        cmds = []
        for prc in prc_list2:
            prc['value'] = base + prc['value']
            cmds.append(prc)

        return cmds