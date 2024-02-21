import mclang.syntax.PrcParser as Prc
import mclang.utils.math_parser as mp

class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        getter, setter = [c.strip() for c in block.split("=", 1)]
        print(getter, setter)