import mclang.syntax.PrcParser as Prc
import mclang.syntax.field as field
import re


regex_list = {
    r"^((?:\w+\.)?(?:\w+))\((.*?)\)$": field.lang_call,
    r"(\w+)\s*=\s*(\w+)": field.lang_varset,
    r"^\s*(\w+)\s*([+\-*/%><~]{1,}=)\s*(\w+)\s*$": field.lang_unary,
}


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        line = f"{base} {block}" # line recovery
        return self.parse_line(line, meta)

    def parse_line(self, line, meta):
        for regex, func in regex_list.items():
            if re.match(regex, line):
                handler = func()
                return handler.parse(line, meta)
        print(f"DEFAULT: {line}")
