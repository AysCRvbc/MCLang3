import mclang.syntax.PrcParser as Prc
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct

class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        ns: Namespace = meta["NMETA"].getNamespace()

        target_func, selector = [s.strip() for s in block.split("->", 1)]
        selector = sct.getSelector(selector, meta)
        target_func = ns.getFunction(target_func)

        modifiers = data.splitlines()

        delete = None

        modifiers_types = {"select": [], "execute": []}
        for mod in modifiers:
            arg = mod.split(" ", 1)[1]
            print(arg)
            mod_base = mod.split(" ")[0]

            if mod_base in modifiers_types:
                modifiers_types[mod_base].append(arg)
            elif mod_base == "delete":
                delete = arg

            # if mod_base == "select":
            #     modifiers_types["select"].append(mod.split(" ", 1)[1])
            # elif mod_base == "delete":
            #     delete = f"{self.meta['name']}_" + mod.split(" ", 1)[1]
            # else:
            #     modifiers_types["execute"].append(mod)

        # modifiers = modifiers_types["select"]

