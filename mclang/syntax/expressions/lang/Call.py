import mclang.syntax.PrcParser as Prc
import re

from mclang.namespace import Namespace


def parse_function_call(line):
    match = re.match(r"^((?:\w+\.)?\w+)\((.*?)\)$", line)
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
            current_argument += char
            in_quotes = not in_quotes
        elif char == "(" or char == "[":
            current_argument += char
            nesting_level += 1
        elif char == ")" or char == "]":
            current_argument += char
            nesting_level -= 1
        else:
            current_argument += char

    arguments.append(current_argument.strip())

    return arguments


class Parser(Prc.PrcParser):
    def alt_parse(self, block, meta, base=None):
        print("Это заявленная функция!")
    def parse(self, block, meta, base=None, data=None):
        data = parse_function_call(block)
        call_name = data['function_name']
        ns: Namespace = meta["NMETA"].getNamespace()

        if call_name in ns.functions:
            return self.alt_parse(block, meta, base)

        caller = None
        func = None
        for var_name in ns.variables:
            var_name += "."
            if call_name.startswith(var_name):
                caller = var_name[:-1]
                if "pointer" not in ns.variables[caller]:
                    caller = None
                    continue
                caller = ns.variables[caller]['pointer']
                func = block[len(var_name):]
                break
        if caller is None:
            raise Exception(f"{call_name} not found")

        call_arguments = data['arguments']
        func = parse_function_call(func)['function_name']
        caller = eval(f"caller.{func}")
        return caller(call_arguments, meta)