import mclang.parser as pr
import mclang.mcjson.parser as mcj

filename = "./mcls/nextbot.mcl"

parser = pr.CodeParser()

res = parser.get_prcs(filename)
pos = "44 10 101"
center = [int(i) for i in pos.split()]
res = mcj.getAllCommandBlocks(res, log=False, center=center)

fastcmd_path = "C:/fastcmd/commands.txt"

ask = input("Загрузить команды в fastcmd? (y/n)")
if ask == "y":
    with open(fastcmd_path, "w") as f:
        for big_cmd in res:
            f.write(big_cmd + "\n")

ask = input("Удалить все блоки команд? (y/n)")
if ask == "y":
    for big_cmd in res:
        new_cmd = big_cmd.split(" ", 4)
        new_cmd[-1] = "air"
        new_cmd = " ".join(new_cmd)
        with open(fastcmd_path, "a") as f:
            f.write(new_cmd + "\n")
