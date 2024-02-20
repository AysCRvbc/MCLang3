import mclang.syntax.PrcParser as Prc
import re


def parse_function_call(line):
    match = re.match(r"^((?:\w+\.)?(?:\w+))\((.*?)\)$", line)
    if not match:
        return None

    function_name = match.group(1)
    arguments = parse_arguments(match.group(2))

    return {
        "function_name": function_name,
        "arguments": arguments,
    }


def parse_arguments(raw_arguments):
    arguments = []
    current_argument = ""
    in_quotes = False
    nesting_level = 0
    for char in raw_arguments:
        if char == "," and nesting_level == 0 and not in_quotes:
            arguments.append(current_argument.strip())
            current_argument = ""
        elif char == "'" or char == '"':
            in_quotes = not in_quotes
        elif char == "(" or char == "[":
            nesting_level += 1
        elif char == ")" or char == "]":
            nesting_level -= 1
        else:
            current_argument += char

    arguments.append(current_argument.strip())

    return arguments


class Parser(Prc.PrcParser):
    def parse(self, block, meta, base=None):
        print("CALL ->", block)
