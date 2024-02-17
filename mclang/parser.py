block_types = {
    "func": 1,
    "input": 1,
    "observer": 1,
    "while": 1,
    "if": 1,
    "else": 1
}

line_types = {
    "@name": 1,
    "@import": 1,
    "var": 1,
    "chat": 1,
    "selector": 1
}


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
                blocks[-1].append(line)
            else:
                blocks.append([line])
                current_tabs = "" if line.startswith("    ") else "    "
    return blocks[1:]


def parse(code: str, parent=""):
    code = preprocess(code)
    code = block_separator(code)

    for block in code:
        is_line = True
        base = block[0].split()[0]
        if base in block_types:
            is_line = False

        print(f"{is_line} => {block}")

    return code
