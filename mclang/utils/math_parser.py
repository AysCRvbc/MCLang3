import ast

from mclang.namespace import Namespace
import mclang.parser as parser


def parse_expression(expression):
    parsed = ast.parse(expression, mode='eval')
    return parsed.body


temp_counter = 0


def get_operator_symbol(op):
    operator_mapping = {
        'Add': '+',
        'Sub': '-',
        'Mult': '*',
        'Div': '/',
        'Pow': '**',
        'Mod': '%',
        'Lt': '<',
        'LtE': '<~',
        'Gt': '>',
        'GtE': '>~',
        'Eq': '~',
    }
    return operator_mapping[op]


def getCallName(call: ast.Call):
    data = call.func
    if isinstance(data, ast.Attribute):
        return getCallName(ast.Call(data.value)) + [data.attr]
    elif isinstance(data, ast.Name):
        return [data.id]
    else:
        raise Exception("Invalid call data")


def getCallData(call: ast.Call):
    name = getCallName(call)
    name = ".".join(name)
    args = [a.id for a in call.args]
    return name, args


def get_math_cmds(expression, meta):
    global temp_counter
    temp_counter = 0

    def generate_temp_var():
        global temp_counter
        temp_var = f'temp_{temp_counter}'
        temp_counter += 1
        return temp_var

    final_result = []
    expression = parse_expression(expression)
    payload = []

    def transform_expression(expr):
        if isinstance(expr, ast.BinOp):
            left = transform_expression(expr.left)
            right = transform_expression(expr.right)
            op = get_operator_symbol(expr.op.__class__.__name__)

            temp_var = generate_temp_var()
            final_result.append(f"{temp_var} = {left}")
            final_result.append(f"{temp_var} {op}= {right}")

            return temp_var
        elif isinstance(expr, ast.UnaryOp):
            operand = transform_expression(expr.operand)
            op = get_operator_symbol(expr.op.__class__.__name__)

            temp_var = generate_temp_var()
            final_result.append(f"{temp_var} = {op}{operand}")

            return temp_var

        elif isinstance(expr, ast.Compare):
            left = transform_expression(expr.left)
            op = [get_operator_symbol(op.__class__.__name__) for op in expr.ops][0]
            right = [transform_expression(comp) for comp in expr.comparators][0]

            temp_var = generate_temp_var()

            final_result.append(f"{temp_var} = {left}")
            final_result.append(f"{temp_var} {op}= {right}")

            return temp_var
        elif isinstance(expr, ast.Call):
            expr: ast.Call
            data = getCallData(expr)
            name = data[0]
            args = data[1]

            ns: Namespace = meta["NMETA"].getNamespace()
            func = ns.getFunction(name, full=True)
            funcns = func['prc'].ns
            prs: parser.CodeParser = meta["PARSER"]
            code = ""
            for i, e in enumerate(args):
                code += f"execute scoreboard players operation @s {funcns.getValue(f'arg{i}')['value']} = @s {ns.getValue(e)['value']}\n"
            code = code.splitlines()
            code.append(f"{name}()")
            payload.extend(code)

            ns.setValue(f"{name}_retval", "scoreboard", meta="dummy")
            ns.getValue(f"{name}_retval")["value"] = funcns.getValue("retval")["value"]

            return f"{name}_retval"

        elif isinstance(expr, ast.Expr):
            return transform_expression(expr.value)
        elif isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.Constant):
            return expr.value
        else:
            raise ValueError(f"Unsupported expression type: {expr.__class__.__name__}")

    temp_var = transform_expression(expression)

    prs: parser.CodeParser = meta["PARSER"]
    for i, e in enumerate(payload):
        payload[i] = prs.parse_code(e)

    return final_result, temp_var, payload
