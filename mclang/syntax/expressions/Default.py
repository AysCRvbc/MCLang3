import mclang.syntax.PrcParser as Prc

regex_list = {
    ""
}


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None):
        line = f"{base} {block}" # line recovery
        return self.parse_line(line, meta)

    def parse_line(self, line, meta):
        print(line)
