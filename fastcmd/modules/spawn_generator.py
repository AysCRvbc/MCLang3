import mclang.syntax.PrcParser as prc
import mclang.parser as pr

class Parser(prc.PrcParser):
    def getName(self):
        return "spawn"

    def parse(self, block, meta, base=None, data=None):
        parser: pr.CodeParser = meta["PARSER"]
        entity_type, call = block.split(" ")

        cmd_first = f"execute summon {entity_type} run "
        call = f"{call}()"
        call, block = parser.parse_prcs(call)

        call['value'] = cmd_first + call['value']
        return [call, block]