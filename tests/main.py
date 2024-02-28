import mclang.parser as pr
import json
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct
import mclang.mcjson.parser as mcj

filename = "examples/main.mcl"

parser = pr.CodeParser()

res = parser.get_prcs(filename)

res = mcj.getBuilding(res, log=True, center=(-16, -61, 11))

for big_cmd in res:
    print(big_cmd)