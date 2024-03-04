import mclang.parser as pr
import mclang.mcjson.parser as mcj

filename = "examples/nextbot.mcl"

parser = pr.CodeParser()

res = parser.get_prcs(filename)

pos = "197 -5 354"

center = [int(i) for i in pos.split()]

res = mcj.getBuilding(res, log=True, center=center, max_cmd=65)

i = 1
print()
for big_cmd in res:
    print(f"{i}. {big_cmd}")
    print()
    l = len(big_cmd)
    print(l)
    if l > 32500:
        print("too long!")
        raise ValueError
    input()
    print()
    i += 1
