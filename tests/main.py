import mclang.parser as pr
import mclang.mcjson.parser as mcj

filename = "examples/pargen.mcl"

parser = pr.CodeParser()

res = parser.get_prcs(filename)

pos = "6 -60 20"

center = [int(i) for i in pos.split()]

res = mcj.getBuilding(res, log=True, center=center)

for big_cmd in res:
    print(big_cmd)
