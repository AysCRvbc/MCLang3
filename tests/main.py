import mclang.parser as parser

filename = "examples/main.mcl"

with open(filename, 'r', encoding='utf-8') as f:
    code = f.read()

res = parser.get_prc_node(code)

print(res)