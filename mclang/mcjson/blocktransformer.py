def getCommandsBlocks(comms, X_center, Y_center, Z_center, chained=True, btype="repeating",
                      x_offset=0, y_offset=0, z_offset=0, conditional=True, facing="up", deletes=False):
    blocks = []
    i = 0
    for cmd in comms:
        cmd = cmd.replace('"', '\\"')
        if chained:
            if i > 0:
                btype = "chain"
        num__ = 1
        if btype is None:
            num__ = 0
        block = f"minecraft:{btype if btype else ''}{'_' * num__}command_block[facing={facing}{',conditional=true'*(btype=='chain' and conditional)}]{{auto: 1b, Command: \"{cmd}\"}} destroy"
        command = f"setblock {X_center + x_offset} {Y_center + i + 1 + y_offset} {Z_center + z_offset} {block}"
        i += 1
        if deletes:
            if cmd.split()[-1] == "None":
                continue
        blocks.append(command)

    return blocks


def fix_quotes(text):
    result = ""
    text = text.replace('\\"', "\\\\\\\"")
    for char in text:
        if char == '"' and result[-1:] != '\\':
            result += "\\"
        result += char
    return result


def commandCombiner(cmds):
    out = ('summon falling_block ~ ~5 ~ {BlockState:{Name:"command_block"},Time:0.01f,TileEntityData:{Command:"%s",'
           'auto:1b},Passengers:[') % fix_quotes(cmds.pop(0))

    for i in cmds:
        out += '{id:"villager",Health:-1,Passengers:['
        out += ('{id:"falling_block",BlockState:{Name:"command_block"},Time:0.01f,TileEntityData:{Command:"%s",auto:1b},'
                'Passengers:[') % fix_quotes(i)

    out = out[:-13] + "}"
    for i in cmds:
        out += "]}"

    out += "]}]}"

    status = len(cmds) - 2

    if status >= 0:
        out += "]}" * status
    else:
        out = out[:status * 2]

    return out
