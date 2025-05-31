from minimizer import print_stage, get_minterms, term_to_string

def get_kmap_index(values):
    if not values: return 0
    binary = int(''.join(map(str, values)), 2)
    return binary ^ (binary >> 1)

def build_kmap(variables, table, size, value=1):
    if size == 0: return [[table[0][0]]]
    row_vars = max(1, size // 2)
    col_vars = size - row_vars
    rows = 1 << row_vars
    cols = 1 << col_vars
    kmap = [[0] * cols for _ in range(rows)]
    terms = get_minterms(variables, table, value)
    for term in terms:
        values = [val for _, val in term]
        row = get_kmap_index(values[:row_vars])
        col = get_kmap_index(values[row_vars:])
        kmap[row][col] = 1
    return kmap

def print_kmap(variables, kmap, row_vars, col_vars):
    print("\nКарта Карно:")
    print(f"Переменные строк: {', '.join(row_vars)}")
    print(f"Переменные столбцов: {', '.join(col_vars)}")
    cols = len(kmap[0])
    col_headers = ['00', '01', '11', '10'] if len(col_vars) == 2 else [str(i) for i in range(cols)]
    print(" " * 6 + " | ".join(col_headers))
    print("-" * (6 + 3 * cols))
    for i, row in enumerate(kmap):
        row_label = f"{row_vars[0]}={i}" if len(row_vars) == 1 else str(i)
        print(f"{row_label:<6} | {' | '.join(map(str, row))}")

def find_groups(kmap, size, value=1):
    rows = len(kmap)
    cols = len(kmap[0]) if rows > 0 else 0
    groups = []
    covered = set()
    def is_valid_group(r, c, h, w):
        for i in range(r, r + h):
            for j in range(c, c + w):
                if kmap[i % rows][j % cols] != value or (i % rows, j % cols) in covered:
                    return False
        return True
    def mark_group(r, c, h, w):
        cells = []
        for i in range(r, r + h):
            for j in range(c, c + w):
                cells.append((i % rows, j % cols))
                covered.add((i % rows, j % cols))
        return cells
    group_sizes = [4, 2, 1]
    for size in group_sizes:
        height = min(size, rows)
        width = size // height if height > 0 else 1
        for r in range(rows):
            for c in range(cols):
                if is_valid_group(r, c, height, width):
                    cells = mark_group(r, c, height, width)
                    groups.append((cells, height, width))
                    if len(groups) >= 2: return groups[:2]
    return groups[:2]

def get_cell_values(size, r, c, variables):
    if size == 3:
        gray_rows = {0: 0, 1: 1}
        gray_cols = {0: (0, 0), 1: (0, 1), 3: (1, 1), 2: (1, 0)}
        a = gray_rows.get(r, 0)
        b, c_val = gray_cols.get(c, (0, 0))
        return {variables[0]: a, variables[1]: b, variables[2]: c_val}
    elif size == 1:
        return {variables[0]: r}
    return {}

def get_constant_vars(cells, size, variables):
    if not cells: return {}
    first_values = get_cell_values(size, cells[0][0], cells[0][1], variables)
    constant_vars = first_values.copy()
    for cell in cells[1:]:
        values = get_cell_values(size, cell[0], cell[1], variables)
        for var in list(constant_vars.keys()):
            if var not in values or constant_vars[var] != values[var]:
                del constant_vars[var]
    return constant_vars

def group_to_implicant(variables, cells, size, is_sdnf):
    constants = get_constant_vars(cells, size, variables)
    if not constants: return "1" if not is_sdnf else "0"
    literals = []
    for var in variables:
        if var in constants:
            val = constants[var]
            literals.append(var if val == (1 if is_sdnf else 0) else f"¬{var}")
    return ("∧" if is_sdnf else "∨").join(literals) or ("0" if is_sdnf else "1")

def minimize_sdnf_kmap(variables, table):
    if not variables: return str(table[0][0])
    size = len(variables)
    if size > 4: return "Слишком много переменных"
    terms = get_minterms(variables, table, 1)
    if not terms: return "0"
    print_stage(1, "Исходные минтермы", [term_to_string(t, True) for t in terms])
    kmap = build_kmap(variables, table, size, value=1)
    row_vars = variables[:max(1, size // 2)]
    col_vars = variables[max(1, size // 2):]
    print_kmap(variables, kmap, row_vars, col_vars)
    groups = find_groups(kmap, size, value=1)
    print_stage(2, "Найденные группы", [f"Группа {i + 1}: {len(g[0])} клеток" for i, g in enumerate(groups)])
    implicants = [group_to_implicant(variables, g[0], size, True) for g in groups]
    print_stage(3, "Результат минимизации", implicants)
    return " ∨ ".join(f"({imp})" for imp in implicants if imp != "0") or "0"

def minimize_sknf_kmap(variables, table):
    if not variables: return str(table[0][0])
    size = len(variables)
    if size > 4: return "Слишком много переменных"
    terms = get_minterms(variables, table, 0)
    if not terms: return "1"
    print_stage(1, "Исходные макстермы", [term_to_string(t, False) for t in terms])
    kmap = build_kmap(variables, table, size, value=0)
    row_vars = variables[:max(1, size // 2)]
    col_vars = variables[max(1, size // 2):]
    print_kmap(variables, kmap, row_vars, col_vars)
    groups = find_groups(kmap, size, value=1)
    print_stage(2, "Найденные группы", [f"Группа {i + 1}: {len(g[0])} клеток" for i, g in enumerate(groups)])
    implicants = [group_to_implicant(variables, g[0], size, False) for g in groups]
    print_stage(3, "Результат минимизации", implicants)
    return " ∧ ".join(f"({imp})" for imp in implicants if imp != "1") or "1"