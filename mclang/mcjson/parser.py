import mclang.mcjson.transformer as tfr
import mclang.mcjson.blocktransformer as btr
import json


def dep_sort(strings):
    with_repeating = [s for s in strings if 'repeating_command_block' in s]
    without_repeating = [s for s in strings if 'repeating_command_block' not in s]

    sorted_strings = sorted(without_repeating) + sorted(with_repeating)

    return sorted_strings


def json_repr_len(dct: dict):
    return len(str(dct))

def getAllCommandBlocks(prcs: list, center, log=False):
    if log:
        k = prcs.copy()
        k.sort(key=json_repr_len, reverse=True)
        print(json.dumps(k, indent=4))

    commands = tfr.transform_mcj(prcs)

    res = []

    x_offset = 0
    triggers = []
    trigger_x = -1

    single_commands = []
    single_commands_x = -1

    for block in commands:
        btype = block['type']

        if btype == "function":
            fblocks = btr.getCommandsBlocks(block['cmds'], *center, x_offset=x_offset, conditional=False, max_y=80)
            res.extend(fblocks)
        elif btype == "command":
            if single_commands_x == -1:
                single_commands_x = x_offset
                x_offset += 1
            command = block['cmds']
            single_commands.append(command)
            x_offset -= 1
        elif btype == "observer":
            if trigger_x == -1:
                trigger_x = x_offset
                x_offset += 1
            triggers.append(block)
            x_offset -= 1

        x_offset += 1

    single_cmds_blocks = btr.getCommandsBlocks(single_commands, *center, x_offset=single_commands_x, chained=False,
                                               btype=None)

    trigger_cmds, delete_cmds = zip(*(block['cmds'] for block in triggers))

    triggerBlocks = btr.getCommandsBlocks(trigger_cmds, *center, x_offset=trigger_x, chained=False, facing="north")
    deleteBlocks = btr.getCommandsBlocks(delete_cmds, *center, x_offset=trigger_x, chained=True, facing="north",
                                         z_offset=-1, deletes=True, btype="chain")

    res.extend(single_cmds_blocks)
    res.extend(triggerBlocks)
    res.extend(deleteBlocks)

    res = dep_sort(res)

    return res


def getBuilding(prcs: list, center=(0, 0, 0), log=False, max_cmd=80):
    res = getAllCommandBlocks(prcs, center=center, log=log)

    return cmdUnifier(res, lim=max_cmd)


def cmdUnifier(cmd: list, lim=70):
    groups = []
    result = []

    maxCommand_in_one_block = lim
    for i in range(0, len(cmd), maxCommand_in_one_block):
        groups.append(cmd[i:i + maxCommand_in_one_block])
    for i in groups:
        i.append(f"fill ~ ~ ~ ~ ~-{len(i) + 1} ~ air")
        result.append(btr.commandCombiner(i))

    return result
