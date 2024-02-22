import mclang.syntax.PrcParser as Prc
from mclang.namespace import Namespace
import mclang.parser as pr


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        res = []
        nmeta: pr.NeccessaryMeta = meta["NMETA"]
        parser: pr.CodeParser = meta["PARSER"]
        ns: Namespace = nmeta.getNamespace()

        if not block:
            block = "None"
        retval_line = f"retval = {block}"
        res.append(retval_line)

        process_name = ns.getFunction(nmeta.process)

        res.append(f"execute tag @s add {process_name}_ended")
        res.append(f"execute tag @s remove {process_name}")

        res = parser.parse_code("\n".join(res))

        return res