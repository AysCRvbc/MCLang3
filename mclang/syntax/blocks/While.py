import mclang.syntax.PrcParser as Prc
import mclang.parser as parser
import mclang.syntax.blocks.Function as func


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
        prs: parser.CodeParser = meta["PARSER"]
        ns: parser.Namespace = nmeta.getNamespace()
        name = f"w{nmeta.level}_{nmeta.index}"
        process = nmeta.process

        funcns = ns.getFunction(process, full=True)['prc'].ns
        ns = funcns

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
""".splitlines()

        base, block = service_code[0].split(" ", 1)
        data = service_code[1:]
        data = [s[4:] for s in data]
        data = "\n".join(data)

        service_prcs = func.Parser(ns=funcns).process(block, meta, base=base, data=data)

