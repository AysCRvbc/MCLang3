# /tellraw @s ["",
# {"text":"Nextbot menu","bold":true,"color":"red"},
# {"text":"\n"},
# {"text":"Summon bot","underlined":true,
#   "clickEvent":
#       {"action":"run_command","value":"/trigger nextbot_input_activate"},
#   "hoverEvent":
#       {"action":"show_text","contents":"Summons DWAYNE ROCK"}},
# {"text":"\n\n"},
# {"text":"Kill all bots","underlined":true,
#   "clickEvent":
#       {"action":"run_command","value":"/trigger nextbot_input_clear"},
#   "hoverEvent":
#   {"action":"show_text","contents":"Command kills every living bot"}}]
#
#
# <color red><bold> Nextbot menu </bold> </color>
# <br>
# <underlined>
# <hover:show_text:Summons DWAYNE ROCK>
# <click:run_command:/trigger nextbot_input_activate>Summon bot</click>
# </hover>
# <br> <br>
# <hover:show_text:Command kills every living bot>
# <click:run_command:/trigger nextbot_input_clear>Kill all bots</click>
# </hover>
# </underlined>

import json


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
                elements.append(input_string[tag_start:i+1])
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
            replaces.append({i: "\n"})
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
                    base["hoverEvent"] = {"action": tag.split(" ", 2)[1].strip(), "contents": tag.split(" ", 2)[2].strip()}
                elif tag_base == "clickEvent":
                    base["clickEvent"] = {"action": tag.split(" ", 2)[1].strip(), "value": tag.split(" ", 2)[2].strip()}
        else:
            res = base.copy()
            res["text"] = i
            result.append(res)

    return result


input_string = """<color red><bold> Nextbot menu </bold> </color>
<br> <underlined>
<hoverEvent show_text Summons DWAYNE ROCK>
<clickEvent run_command /trigger nextbot_input_activate>Summon bot</clickEvent> </hoverEvent>
<br> <br>
<hoverEvent show_text Command kills every living bot"> <clickEvent run_command /trigger nextbot_input_clear)>Kill all bots</clickEvent>
</hoverEvent>
</underlined>
"""

elements = getElements(input_string)
print(elements_to_json(elements))

