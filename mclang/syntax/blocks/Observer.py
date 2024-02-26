import mclang.syntax.PrcParser as Prc
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct
import mclang.parser as parser


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None, data=None):
        nmeta: parser.NeccessaryMeta = meta["NMETA"]
        ns: Namespace = nmeta.getNamespace()

        target_func, selector = [s.strip() for s in block.split("->", 1)]
        selector = sct.getSelector(selector, meta)
        target_func = ns.getFunction(target_func)

        modifiers = data.splitlines()

        delete = None

        modifiers_types = {"select": [], "execute": []}
        for mod in modifiers:
            arg = mod.split(" ", 1)[1]
            mod_base = mod.split(" ")[0]

            if mod_base in modifiers_types:
                modifiers_types["select"].append(arg)
            elif mod_base == "delete":
                delete = arg
            else:
                modifiers_types["execute"].append(mod)

        modifiers = modifiers_types["select"]
        additionals = modifiers_types["execute"]

        old_mods = selector.split("[", 1)
        if len(old_mods) > 1:
            base_sct = old_mods[0]
            old_mods = old_mods[1]
            old_mods = sct.parse_arguments(old_mods)
            old_mods.extend(modifiers)
            new_mods = ",".join(old_mods)
            new_mods = f"[{new_mods}]"
            selector = f"{base_sct}{new_mods}"
        else:
            new_mods = ",".join(modifiers)
            new_mods = f"[{new_mods}]"
            selector = f"{selector}{new_mods}"

        selector = sct.getSelector(selector, meta)

        res = {
            "call": target_func,
            "selector": selector,
            "additionals": additionals,
            "delete": delete
        }

        nmeta.addCompiled(res)

