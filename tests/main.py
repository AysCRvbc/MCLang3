# import mclang.parser as parser
#
# filename = "examples/main.mcl"
#
# with open(filename, 'r', encoding='utf-8') as f:
#     code = f.read()
#
# for i in parser.parse(code):
#     print(repr(i))


import mclang.namespace as ns

namespace = ns.Namespace("cctest")

namespace.setValue("y_d")
namespace.setFunction("checker")

new_ns = namespace.copy("check")

new_ns.setLocal("y_d")
new_ns.setFunction("lmao.getlife")

print(namespace.variables)
print(namespace.functions)

print(new_ns.variables)
print(new_ns.functions)
