import ast


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


def get_math_cmds(expression):
    global temp_counter
    temp_counter = 0

    def generate_temp_var():
        global temp_counter
        temp_var = f'temp_{temp_counter}'
        temp_counter += 1
        return temp_var

    final_result = []
    expression = parse_expression(expression)

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
        elif isinstance(expr, ast.Expr):
            return transform_expression(expr.value)
        elif isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.Constant):
            return expr.value
        else:
            raise ValueError(f"Unsupported expression type: {expr.__class__.__name__}")

    temp_var = transform_expression(expression)

    return final_result, temp_var