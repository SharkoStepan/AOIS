import re
from itertools import product

def replace_impl(expr):
    expr = expr.replace(" ", "")
    while '->' in expr:
        impl_pos = expr.find('->')
        left = find_left_operand(expr, impl_pos - 1)
        right = find_right_operand(expr, impl_pos + 2)
        expr = expr.replace(f"{left}->{right}", f"(not {left} or {right})")
    return expr

def find_left_operand(expr, end):
    if end < 0: return ""
    if expr[end] == ')':
        balance = 1
        start = end
        while balance != 0 and start > 0:
            start -= 1
            if expr[start] == '(': balance -= 1
            elif expr[start] == ')': balance += 1
        return expr[start:end + 1] if balance == 0 else ""
    elif expr[end] == '!': return '!' + find_left_operand(expr, end - 1)
    elif expr[end].isalpha(): return expr[end]
    return ""

def find_right_operand(expr, start):
    if start >= len(expr): return ""
    if expr[start] == '(':
        balance = 1
        end = start + 1
        while balance != 0 and end < len(expr):
            if expr[end] == '(': balance += 1
            elif expr[end] == ')': balance -= 1
            end += 1
        return expr[start:end] if balance == 0 else ""
    elif expr[start] == '!': return '!' + find_right_operand(expr, start + 1)
    elif expr[start].isalpha(): return expr[start]
    return ""

def expr_to_python(expr, var_values):
    expr = replace_impl(expr)
    for var, val in var_values.items():
        expr = re.sub(r'\b' + re.escape(var) + r'\b', str(bool(val)), expr)
    expr = expr.replace('!', 'not ')
    expr = expr.replace('&', ' and ')
    expr = expr.replace('|', ' or ')
    return expr

def eval_expr(expr, var_values):
    try:
        python_expr = expr_to_python(expr, var_values)
        return int(bool(eval(python_expr)))
    except: raise ValueError("Ошибка вычисления")

def generate_truth_table(expr):
    expr = expr.replace(" ", "")
    if expr in ['0', '1']: return [], [[int(expr)]]
    variables = sorted(set(re.findall(r'\b[a-e]\b', expr)))
    if not variables: raise ValueError("Нет переменных")
    table = []
    for values in product([0, 1], repeat=len(variables)):
        var_values = dict(zip(variables, values))
        result = eval_expr(expr, var_values)
        table.append(list(values) + [result])
    return variables, table

def print_truth_table(variables, table):
    if not variables:
        print("f\n-\n" + str(table[0][0]))
        return
    header = " | ".join(variables + ['f'])
    print(header)
    print("-" * len(header))
    for row in table:
        print(" | ".join(map(str, row)))