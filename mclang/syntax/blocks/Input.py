import mclang.syntax.PrcParser as Prc
import mclang.syntax.expressions.Selector as sct
from mclang.namespace import Namespace
import mclang.parser as prs


#init_block = [f"var trigger input_{raw_name}"]
# triggerGiver_block = [f'observe {selector} -> {name}_tag_giver',
#                       f'    select tag = !{name}_tag', ]
# funcGiver_block = [f'func {name}_tag_giver() -> {selector}',
#                    f'    /scoreboard players enable @s {self.name}',
#                    f'    self.{name}_tag = true', ]
# triggerActive_block = [f'observe {selector} -> {name}_function',
#                        f'    unless score @s {self.name} matches 0']
# funcActive_block = [f'func {name}_function() -> {selector}',
#                     f'    {arg} = input_{raw_name}',
#                     f'    input_{raw_name} = 0',
#                     f'    self.{name}_tag = false']
class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: prs.CodeParser = meta["PARSER"]

        definer = block.split("(", 2)
        args = [arg.strip() for arg in definer[1].split(")")[0].split(",")]
        args = [arg for arg in args if arg]
        assert len(args) == 1

        raw_name = definer[0]
        arg = args[0]
        selector = block.split("->")[1].strip()
        name = f"input_{raw_name}"

        prcs = []

        code_block = [f"var input_{raw_name} trigger"]

        prcs.append(parser.parse_code("\n".join(code_block)))


        code_block = [f'func {name}_tag_giver() -> {selector}',
                            f'    execute scoreboard players enable @s {ns.getValue(f"input_{raw_name}")["value"]}',
                            f'    self.{name}_tag = True']

        prcs.append(parser.parse_code("\n".join(code_block)))

        code_block = [f'func {name}_function() -> {selector}',
                            f'    {arg} = input_{raw_name}',
                            f'    input_{raw_name} = 0',
                            f'    self.{name}_tag = False']
        code_block.extend([ f'    {cmd}' for cmd in data.splitlines()])

        prcs.append(parser.parse_code("\n".join(code_block)))

        code_block = [f'observe {name}_tag_giver -> {selector}',
                      f'    select tag = !{name}_tag']

        prcs.append(parser.parse_code("\n".join(code_block)))

        code_block = [f'observe {name}_function -> {selector}',
                      f'    unless score @s {ns.getValue(f"input_{raw_name}")["value"]} matches 0']

        prcs.append(parser.parse_code("\n".join(code_block)))