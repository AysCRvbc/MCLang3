import mclang.parser as pr

filename = "examples/main.mcl"

parser = pr.CodeParser()

res = parser.get_prc_node(filename)

print(res)