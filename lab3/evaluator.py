from typing import List


def shunting_yard(tokens: list[str]) -> list[str]:
    output = []
    op_stack = []
    priority = {"!": 5, "~": 4, "&": 3, "|": 2, "->": 1, "(": 0}

    for token in tokens:
        if token == "(":
            op_stack.append(token)
        elif token == ")":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            op_stack.pop()
        elif token in priority:
            while op_stack and priority.get(op_stack[-1], 0) >= priority[token]:
                output.append(op_stack.pop())
            op_stack.append(token)
        else:
            output.append(token)

    while op_stack:
        output.append(op_stack.pop())

    return output


def evaluate_postfix(postfix: list[str], vars: dict[str, bool]) -> bool:
    stack = []
    for token in postfix:
        if len(token) == 1 and 'a' <= token <= 'e':
            stack.append(vars[token])
        elif token in ["!", "&", "|", "->", "~"]:
            try:
                if token == "!":
                    a = stack.pop()
                    stack.append(not a)
                elif token == "&":
                    if len(stack) < 2:
                        raise ValueError("Not enough operands for &")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a and b)
                elif token == "|":
                    if len(stack) < 2:
                        raise ValueError("Not enough operands for |")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a or b)
                elif token == "->":
                    if len(stack) < 2:
                        raise ValueError("Not enough operands for ->")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(not a or b)
                elif token == "~":
                    if len(stack) < 2:
                        raise ValueError("Not enough operands for ~")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append((not a or b) and (not b or a))
            except IndexError:
                raise ValueError("Not enough operands in stack")
        else:
            raise ValueError("Unknown token")
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]


def generate_truth_table(variables: list[str], postfix: list[str]) -> list[list[bool]]:
    n = len(variables)
    rows = 1 << n
    table = []

    for i in range(rows):
        var_values = {}
        for j in range(n):
            value = bool((i >> (n - 1 - j)) & 1)
            var_values[variables[j]] = value

        row = [var_values[var] for var in variables]
        row.append(evaluate_postfix(postfix, var_values))
        table.append(row)

    return table


def generate_sdnf(variables: list[str], table: list[list[bool]]) -> str:
    terms = []
    for row in table:
        if row[-1]:
            literals = []
            for i, var in enumerate(variables):
                literals.append(var if row[i] else f"!{var}")
            terms.append(f"({' & '.join(literals)})")
    if not terms:
        return "Always False"
    return " | ".join(terms)


def generate_sknf(variables: list[str], table: list[list[bool]]) -> str:
    terms = []
    for row in table:
        if not row[-1]:
            literals = []
            for i, var in enumerate(variables):
                literals.append(f"!{var}" if row[i] else var)
            terms.append(f"({' | '.join(literals)})")
    if not terms:
        return "Always True"
    return " & ".join(terms)


def generate_sdnf_numeric(table: list[list[bool]]) -> list[int]:
    return [i for i, row in enumerate(table) if row[-1]]


def generate_sknf_numeric(table: list[list[bool]]) -> list[int]:
    return [i for i, row in enumerate(table) if not row[-1]]


def format_numeric(terms: list[int]) -> str:
    return ", ".join(map(str, terms)) if terms else "null"


def generate_index_form(table: list[list[bool]]) -> int:
    index = 0
    bits = len(table)
    for i, row in enumerate(table):
        if row[-1]:
            index |= (1 << (bits - 1 - i))
    return index


def print_minimization_stages(stages: List[List[str]], title: str):
    print(f"\n{title} stages:")
    for i, stage in enumerate(stages, 1):
        print(f"Stage {i}:")
        for step in stage:
            print(f"  {step}")


def print_truth_table(variables: list[str], table: list[list[bool]]):
    print(" ".join(variables) + " | Result")
    print("-" * (len(variables) * 2 + 3 + 10))

    for row in table:
        print(" ".join(["1" if x else "0" for x in row[:-1]]) + " | " + ("1" if row[-1] else "0"))

    sdnf = generate_sdnf(variables, table)
    sknf = generate_sknf(variables, table)
    print(f"\nDNF: {sdnf}")
    print(f"CNF: {sknf}")

    sdnf_numeric = generate_sdnf_numeric(table)
    sknf_numeric = generate_sknf_numeric(table)
    print(f"Numeric DNF: {format_numeric(sdnf_numeric)}")
    print(f"Numeric CNF: {format_numeric(sknf_numeric)}")

    index = generate_index_form(table)
    binary_str = "".join(["1" if row[-1] else "0" for row in table])
    print(f"Index Form: {index} - {binary_str}")

    from minimizer import (
        minimize_sdnf, minimize_sknf,
        minimize_with_karnaugh_sdnf, minimize_with_karnaugh_sknf,
        minimize_quine_mccluskey_sdnf, minimize_quine_mccluskey_sknf
    )

    minimized_sdnf, sdnf_stages = minimize_sdnf(sdnf_numeric, len(variables))
    minimized_sknf, sknf_stages = minimize_sknf(sknf_numeric, len(variables))

    karnaugh_sdnf, karnaugh_sdnf_stages = minimize_with_karnaugh_sdnf(sdnf_numeric, len(variables))
    karnaugh_sknf, karnaugh_sknf_stages = minimize_with_karnaugh_sknf(sknf_numeric, len(variables))

    quine_sdnf, quine_sdnf_stages = minimize_quine_mccluskey_sdnf(sdnf_numeric, len(variables))
    quine_sknf, quine_sknf_stages = minimize_quine_mccluskey_sknf(sknf_numeric, len(variables))

    print(f"\nMinimized DNF (calculation method): {minimized_sdnf}")
    print_minimization_stages(sdnf_stages, "DNF minimization (calculation method)")

    print(f"\nMinimized CNF (calculation method): {minimized_sknf}")
    print_minimization_stages(sknf_stages, "CNF minimization (calculation method)")

    print(f"\nMinimized DNF (Karnaugh map): {karnaugh_sdnf}")
    print_minimization_stages(karnaugh_sdnf_stages, "DNF minimization (Karnaugh map)")

    print(f"\nMinimized CNF (Karnaugh map): {karnaugh_sknf}")
    print_minimization_stages(karnaugh_sknf_stages, "CNF minimization (Karnaugh map)")

    print(f"\nMinimized DNF (Quine-McCluskey): {quine_sdnf}")
    print_minimization_stages(quine_sdnf_stages, "DNF minimization (Quine-McCluskey)")

    print(f"\nMinimized CNF (Quine-McCluskey): {quine_sknf}")
    print_minimization_stages(quine_sknf_stages, "CNF minimization (Quine-McCluskey)")