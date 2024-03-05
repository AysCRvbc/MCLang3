import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace
import mclang.syntax.expressions.Selector as sct


def getElements(input_string):
    result = ""
    start_tag = False
    tag_start = 0
    elements = []
    current = ""
    prev = ""

    input_string = input_string.replace("\n", "")

    for i, c in enumerate(input_string):
        if start_tag:
            if c == ">" and prev != "\\":
                start_tag = False
                elements.append(input_string[tag_start:i + 1])
        else:
            if c == "<" and prev != "\\":
                current = current.strip()
                if current:
                    elements.append(current)
                current = ""
                start_tag = True
                tag_start = i
            else:
                current += c

        result += c
        prev = c

    replaces = []
    for i, e in enumerate(elements):
        if e == "<br>":
            replaces.append({i: "\\n"})
        stripped = e.strip()
        if e != stripped:
            replaces.append({i: stripped})

    for i in replaces:
        key = list(i.keys())[0]
        elements[key] = i[key]

    return elements


def elements_to_json(elements):
    result = []
    base = {}

    for i in elements:
        if i.startswith("<"):
            tag = i[1:-1]
            if tag[0] == "/":
                tag = tag[1:]
                if tag == "color":
                    base['color'] = "white"
                else:
                    base.pop(tag)
            else:
                tag_base = tag.split()[0]
                if tag_base == "color":
                    color = tag.split(" ", 1)[1]
                    base["color"] = color
                elif tag_base == "bold":
                    base["bold"] = True
                elif tag_base == "italic":
                    base["italic"] = True
                elif tag_base == "strikethrough":
                    base["strikethrough"] = True
                elif tag_base == "underlined":
                    base["underlined"] = True
                elif tag_base == "obfuscated":
                    base["obfuscated"] = True
                elif tag_base == "hoverEvent":
                    base["hoverEvent"] = {"action": tag.split(" ", 2)[1].strip(),
                                          "contents": tag.split(" ", 2)[2].strip()}
                elif tag_base == "clickEvent":
                    base["clickEvent"] = {"action": tag.split(" ", 2)[1].strip(), "value": tag.split(" ", 2)[2].strip()}
        else:
            res = base.copy()
            res["text"] = i
            result.append(res)

    return result


class Parser(prc.PrcParser):
    def __init__(self):
        self.templatePath = None

    def getName(self):
        return "tellrope"

    def parse(self, block, meta, base=None, data=None):
        nmeta: pr.NeccessaryMeta = meta["NMETA"]
        ns: Namespace = nmeta.getNamespace()
        varname, path = [x.strip() for x in block.split("=")]
        self.templatePath = eval(path)

        ns.setValue(varname, "tellrope")
        ns.getValue(varname)["pointer"] = self

    def show(self, args, meta):
        selector = args[0]
        selector = sct.getSelector(selector, meta)

        with open(self.templatePath, "r", encoding="utf-8") as f:
            text = f.read()
            elements = getElements(text)
            json = elements_to_json(elements)

        json = str(json).replace("'", '"')

        cmd = f"tellraw {selector} {json}"
        res = {"type": "command", "value": cmd}

        return [res]