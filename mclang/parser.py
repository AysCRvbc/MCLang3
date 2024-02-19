from mclang.syntax.field import *
from typing import Type
from mclang.syntax.PrcParser import PrcParser

block_types = {
    "func": func_block,
    "input": input_block,
    "observer": observer_block,
    "while": while_block,
    "if": if_block,
    "else": else_block
}

line_types = {
    "@name": config,
    "@import": config,
    "var": var,
    "chat": chat,
    "selector": selector,
    "execute": execute,
}


def get_parser(base) -> Type[PrcParser]:
    if base in block_types:
        return block_types[base]
    elif base in line_types:
        return line_types[base]
    else:
        return default


def preprocess(code: str):
    def delete_comment(line: str):
        res = ""
        is_str = False
        for c in line:
            if c == '"':
                is_str = not is_str
            if not is_str and c == '#':
                break
            res += c
        return res

    lines = code.splitlines()
    lines = [delete_comment(line) for line in lines]
    lines = [line.rstrip() for line in lines if line]
    return "\n".join(lines)


def block_separator(mcc_code):
    blocks = [[]]
    current_tabs = "    "
    for line in mcc_code.split("\n"):
        if line.strip():
            if line.startswith(current_tabs):
                if len(blocks[-1]):
                    blocks[-1].append("")
                blocks[-1][1] += f"{line[4:]}\n"
            else:
                blocks.append([line])
                current_tabs = "" if line.startswith("    ") else "    "
    return blocks[1:]


meta = {}


def parse_block(block):
    base, args = block[0].split(" ", 1)
    prcparser = get_parser(base)()
    prc = prcparser.parse(args, meta)


def get_prc_node(code):
    code = preprocess(code)
    result = parse_code(code)
    return result


def parse_code(code: str):
    code = block_separator(code)
    prc_list = []
    for block in code:
        prc_list.append(parse_block(block))

    return code
