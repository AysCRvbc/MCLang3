import mclang.syntax.PrcParser as Prc
import mclang.syntax.expressions.lang.VariableSet as vs

class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        code = f"temp = {block}"
        prs_code = vs.Parser().parse(code, meta)
