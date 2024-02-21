import mclang.parser as pr
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct

filename = "examples/main.mcl"

parser = pr.CodeParser()

res = parser.get_prc_node(filename)

print(res)
# ns: Namespace = parser.NMeta.getNamespace()
# for val, key in ns.variables.items():
#     print(val, key)
