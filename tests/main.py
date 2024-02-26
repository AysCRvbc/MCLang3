import mclang.parser as pr
import json
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct

filename = "examples/main.mcl"

parser = pr.CodeParser()

res = parser.get_prcs(filename)

# print(json.dumps(res, indent=2))
