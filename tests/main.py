import mclang.parser as parser

filename = "examples/main.mcl"

with open(filename, 'r', encoding='utf-8') as f:
    code = f.read()

parser.parse(code)

