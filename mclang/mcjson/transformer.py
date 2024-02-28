import mclang.syntax.expressions.Selector as sct


def transform_mcj(mcj: list):
    res = []

    def add(ptype, commands):
        res.append({"type": ptype, "cmds": commands})

    for prc in mcj:
        prctype = prc['type']
        if prctype == "function":
            add("function", getFunctionCommands(prc))
        elif prctype == "command":
            add("command", prc['value'])
        elif prctype == "observer":
            add("observer", getObserverCommands(prc))

    return res


def getFunctionCommands(prc: dict):
    res = []
    cmds = prc['data']
    name = prc['name']
    selector = prc['selector']

    cmds.append(f"tag @s remove {prc['name']}")

    if "[" in selector:
        selector_base, selector_temp = selector.split("[", 1)
        selector_args = sct.parse_arguments(selector_temp)
        selector_args.append(f"tag={name}")
        selector = f"{selector_base}[{','.join(selector_args)}]"
    else:
        selector = f"{selector}[tag={name}]"

    base_cmd = f"execute as {selector} run "
    for cmd in cmds:
        res.append(base_cmd + cmd)

    return res


def getObserverCommands(prc: dict):
    name = prc['call']
    selector = prc['selector']
    additionals = prc['additionals']
    delete = prc['delete']

    cycling_cmd = f"execute as {selector}{' ' + ''.join(additionals) if additionals else ''} run tag @s add {name}"
    delete_cmd = f"execute as {selector}{' ' + ''.join(additionals) if additionals else ''} run tag @s remove {delete}"

    return [cycling_cmd, delete_cmd]
