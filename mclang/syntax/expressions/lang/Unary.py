import re
import mclang.syntax.PrcParser as Prc


def parse_string(input_string):
    pattern = re.compile(r'^\s*(\w+)\s*([+\-*/%><~]{1,}=)\s*(\w+)\s*$')

    match = pattern.match(input_string)

    if match:
        varname_1 = match.group(1)
        operation = match.group(2)
        varname_2 = match.group(3)

        return True, varname_1, operation, varname_2
    else:
        return False, None, None, None


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        print("Unary operation: ", end="")
        print(parse_string(block))