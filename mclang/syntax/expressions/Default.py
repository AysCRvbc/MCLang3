import mclang.syntax.PrcParser as Prc
import mclang.syntax.field as field
import re


regex_list = {
    r"^((?:\w+\.)?(?:\w+(?:\.\w+)*))\((.*?)\)$": field.lang_call,
    r"(?P<arg1>\b\w+(?:\.\w+)*)\s*=\s*(?P<arg2>\b\w+(?:\.\w+)*)\b": field.lang_varset,
    r'(?P<arg1>\b\w+(?:\.\w+)*)\s*(?P<operator>\+|-|/|\*|%|>|<|>~|<~|~)=\s*(?P<arg2>\b\w+(?:\.\w+)*|\d+)\b': field.lang_unary,
}


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        line = f"{base} {block}" # line recovery
        line = line.strip()
        return self.parse_line(line, meta)

    def parse_line(self, line, meta):
        for regex, func in regex_list.items():
            res = re.match(regex, line)
            if res:
                handler = func()
                return handler.parse(line, meta)
        raise Exception("Syntax error in line: " + line)
