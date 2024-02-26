import mclang.syntax.PrcParser as Prc
import mclang.parser as parser

# service_function = f"""func {self.name}() -> {selector}
#     if {self.condition}
#     {code}
#         >{self.name}
#     else
#         return"""
class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
        prs: parser.CodeParser = meta["PARSER"]
        ns: parser.Namespace = nmeta.getNamespace()
        name = f"{nmeta.process}_{nmeta.level}_{nmeta.index}w"
        process = nmeta.process

        if process == "Main":
            selector = "@e"
        else:
            parent = ns.getFunction(process, full=True)['prc']
            selector = parent.selector

        code = data
        newline = "\n"

        service_code = f"""func {name}() -> {selector}
    if {block}
        {f'{newline}        '.join(code.splitlines())}
        {name}()
    else
        return 
"""
        print(service_code)
        service_prcs = prs.parse_prcs(service_code)
