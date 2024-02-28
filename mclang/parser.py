import os

from mclang.namespace import Namespace
import mclang.namespace as nslib
from mclang.syntax.field import *
from typing import Type
from mclang.syntax.PrcParser import PrcParser


class NeccessaryMeta:
    def __init__(self):
        self.service_blocks = []
        self.service_compiled = []
        self.namespace = None
        self.process: str = "Main"
        self.prevBlock = None

        self.level = 0
        self.index = 0

    def setNamespace(self, namespace_name):
        if self.namespace is not None:
            self.namespace = self.namespace.copy(namespace_name)
            return
        self.namespace = Namespace(namespace_name)
        return self.namespace

    def setProcess(self, process):
        self.process = process

    def clearProcess(self):
        self.process = "Main"

    def getNamespace(self, local=False):
        if self.namespace is None:
            raise ValueError("Namespace is None")
        if local:
            func = self.process
            ns = self.namespace.getFunction(func, full=True)['prc'].ns
            return ns
        return self.namespace

    def addBlock(self, block):
        self.service_blocks.append(block)

    def addCompiled(self, compiled: dict):
        self.service_compiled.append(compiled)

    def bulk_addCompiled(self, compiled: list):
        for c in compiled:
            self.addCompiled(c)

    def parse_service_prc(self, meta_dict, cparser):
        if not self.service_blocks:
            return None
        res = self.service_blocks[0]
        res = cparser.parse_block(res, meta_dict)
        self.service_blocks.pop(0)
        return res


block_types = {
    "func": func_block,
    "input": input_block,
    "observe": observer_block,
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
    "return": return_expr
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
    for i, block in enumerate(blocks):
        blocks[i] = block[:2]
    return blocks[1:]


def recursive_array_unpack(array):
    res = []
    for el in array:
        if isinstance(el, list):
            res.extend(recursive_array_unpack(el))
        else:
            res.append(el)
    return res


class CodeParser:
    def __init__(self, parent=None):
        self.NMeta = NeccessaryMeta()
        self.meta = {"NMETA": self.NMeta, "PARSER": self}
        if parent is not None:
            self.NMeta.setNamespace(parent)

    def parse_block(self, block, meta_dict):
        base = block[0].split(" ", 1)
        if len(base) == 1:
            args = ""
        else:
            args = base[1]
        base = base[0]

        prcparser = get_parser(base)()
        try:
            prc = prcparser.process(args, meta_dict, base=base, data=block[-1])
        except Exception as e:
            print(e)
            prcparser = default()
            prc = prcparser.process(args, meta_dict, base=base, data=block[-1])
        return prc

    def parse_prcs(self, code: str):
        code = preprocess(code)
        result = self.parse_code(code)
        result = [prc for prc in result if prc]
        result = recursive_array_unpack(result)
        return result

    def get_prcs(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        abs_path = file_path if file_path.startswith("/") else os.path.abspath(file_path)
        folder_path = os.path.dirname(abs_path) + "/"

        self.meta["path"] = folder_path

        prc_list = self.parse_prcs(code)

        while self.NMeta.service_blocks:
            prc_list.append(self.NMeta.parse_service_prc(self.meta, self))
        prc_list.extend(self.NMeta.service_compiled)

        for i in nslib.scoreboard_variables:
            prc_list.insert(0,
                    {"type": "command",
                             "value": f"scoreboard objectives add {i['value']} {i['objectives']}"})

        return prc_list

    def parse_code(self, code: str):
        code = block_separator(code)
        prc_list = []
        for block in code:
            prc_list.append(self.parse_block(block, self.meta))

        return prc_list
