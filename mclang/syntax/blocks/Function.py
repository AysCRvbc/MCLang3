import mclang.syntax.PrcParser as Prc
import mclang.parser as parser

class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        prs = parser.CodeParser()