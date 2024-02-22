import mclang.syntax.PrcParser as Prc
import mclang.utils.math_parser as mp

class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        getter, setter = [c.strip() for c in block.split("=", 1)]
        setter = mp.get_math_cmds(setter)
        code = f"{getter} = {setter[1]}"
        if len(setter[0]) != 0:
            code = setter[0]
            code.append(f"{getter} = {setter[1]}")
            code = "\n".join(code)
            return meta["PARSER"].parse_code(code)
        else:
            return self.setOperation(code, meta)

    def setOperation(self, block, meta):
        print(block)
        return None