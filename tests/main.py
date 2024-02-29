import mclang.parser as pr
import json
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct
import mclang.mcjson.parser as mcj

filename = "examples/main.mcl"

parser = pr.CodeParser()

res = parser.get_prcs(filename)

pos = "6 -12 20"

center = [int(i) for i in pos.split()]

res = mcj.getBuilding(res, log=False, center=center)

for big_cmd in res:
    print(big_cmd)
