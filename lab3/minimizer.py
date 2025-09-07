from typing import List, Tuple, Set


def get_binary(minterm: int, num_vars: int) -> str:
    return bin(minterm)[2:].zfill(num_vars)


def count_ones(binary: str) -> int:
    return binary.count('1')


def can_combine(a: str, b: str) -> Tuple[bool, str]:
    diff = 0
    combined = []
    for bit_a, bit_b in zip(a, b):
        if bit_a != bit_b:
            diff += 1
            combined.append('-')
        else:
            combined.append(bit_a)
        if diff > 1:
            return (False, '')
    return (diff == 1, ''.join(combined))


def find_prime_implicants(minterms: List[int], num_vars: int) -> Tuple[List[Tuple[str, Set[int]]], List[List[str]]]:
    if not minterms:
        return [], []

    groups = {}
    for m in minterms:
        binary = get_binary(m, num_vars)
        cnt = count_ones(binary)
        if cnt not in groups:
            groups[cnt] = []
        groups[cnt].append((binary, {m}))

    prime_implicants = []
    all_stages = []

    while True:
        new_groups = {}
        stage_results = []
        used = set()

        keys = sorted(groups.keys())
        for i in range(len(keys) - 1):
            group1 = groups[keys[i]]
            group2 = groups[keys[i + 1]]

            for (a, a_terms) in group1:
                for (b, b_terms) in group2:
                    can_comb, combined = can_combine(a, b)
                    if can_comb:
                        new_terms = a_terms.union(b_terms)
                        cnt = count_ones(combined)
                        if cnt not in new_groups:
                            new_groups[cnt] = []
                        new_groups[cnt].append((combined, new_terms))
                        used.update(a_terms)
                        used.update(b_terms)
                        stage_results.append(f"{a} + {b} -> {combined} (terms: {new_terms})")

        for group in groups.values():
            for (pattern, terms) in group:
                if not terms.issubset(used):
                    prime_implicants.append((pattern, terms))

        if not stage_results:
            break

        all_stages.append(stage_results)
        groups = new_groups

    return prime_implicants, all_stages


def get_essential_primes(primes: List[Tuple[str, Set[int]]], minterms: Set[int]) -> List[Tuple[str, Set[int]]]:
    if not primes or not minterms:
        return []

    coverage = {m: [] for m in minterms}
    for pi in primes:
        for m in pi[1]:
            if m in minterms:
                coverage[m].append(pi)

    essential = []
    remaining_minterms = set(minterms)

    for m in list(remaining_minterms):
        if len(coverage[m]) == 1:
            pi = coverage[m][0]
            if pi not in essential:
                essential.append(pi)
                remaining_minterms.difference_update(pi[1])

    while remaining_minterms:
        best_pi = None
        best_coverage = 0
        for pi in primes:
            if pi in essential:
                continue
            covered = pi[1].intersection(remaining_minterms)
            if len(covered) > best_coverage:
                best_pi = pi
                best_coverage = len(covered)

        if best_pi:
            essential.append(best_pi)
            remaining_minterms.difference_update(best_pi[1])
        else:
            break

    return essential


def pattern_to_expression(pattern: str, variables: List[str], is_dnf: bool) -> str:
    literals = []
    for i, bit in enumerate(pattern):
        if bit == '0':
            literals.append(f"!{variables[i]}" if is_dnf else variables[i])
        elif bit == '1':
            literals.append(variables[i] if is_dnf else f"!{variables[i]}")
    return " & ".join(literals) if is_dnf else " | ".join(literals)


def minimize_sdnf(minterms: List[int], num_vars: int) -> Tuple[str, List[List[str]]]:
    primes, stages = find_prime_implicants(minterms, num_vars)
    essential_primes = get_essential_primes(primes, set(minterms))

    if not essential_primes:
        return "Always False", stages

    variables = [chr(ord('a') + i) for i in range(num_vars)]
    terms = []

    for pi in essential_primes:
        term = pattern_to_expression(pi[0], variables, True)
        terms.append(f"({term})")

    minimized = " | ".join(terms) if terms else "Always False"
    return minimized, stages


def minimize_sknf(maxterms: List[int], num_vars: int) -> Tuple[str, List[List[str]]]:
    primes, stages = find_prime_implicants(maxterms, num_vars)
    essential_primes = get_essential_primes(primes, set(maxterms))

    if not essential_primes:
        return "Always True", stages

    variables = [chr(ord('a') + i) for i in range(num_vars)]
    terms = []

    for pi in essential_primes:
        term = pattern_to_expression(pi[0], variables, False)
        terms.append(f"({term})")

    minimized = " & ".join(terms) if terms else "Always True"
    return minimized, stages


def get_karnaugh_map_size(num_vars: int) -> Tuple[int, int]:
    if num_vars == 2:
        return 2, 2
    elif num_vars == 3:
        return 2, 4
    elif num_vars == 4:
        return 4, 4
    else:
        rows = 1 << (num_vars // 2)
        cols = 1 << ((num_vars + 1) // 2)
        return rows, cols


def build_karnaugh_map(minterms: List[int], num_vars: int) -> List[List[int]]:
    rows, cols = get_karnaugh_map_size(num_vars)
    k_map = [[0 for _ in range(cols)] for _ in range(rows)]

    def get_coordinates(num_bits):
        gray = []
        for i in range(1 << num_bits):
            gray.append(i ^ (i >> 1))
        return [format(g, f'0{num_bits}b') for g in gray]

    row_bits = num_vars // 2
    col_bits = (num_vars + 1) // 2
    row_gray = get_coordinates(row_bits)
    col_gray = get_coordinates(col_bits)

    for i in range(rows):
        for j in range(cols):
            if num_vars == 1:
                binary = row_gray[i]
            elif num_vars == 2:
                binary = row_gray[i][0] + col_gray[j][0]
            elif num_vars == 3:
                binary = row_gray[i][0] + col_gray[j][0] + col_gray[j][1]
            elif num_vars == 4:
                binary = row_gray[i][0] + row_gray[i][1] + col_gray[j][0] + col_gray[j][1]
            else:
                binary = row_gray[i][0] + row_gray[i][1] + col_gray[j][0] + col_gray[j][1] + col_gray[j][2]

            decimal = int(binary, 2)
            k_map[i][j] = 1 if decimal in minterms else 0

    return k_map


def find_karnaugh_groups(k_map: List[List[int]]) -> List[Tuple[int, int, int, int]]:
    rows = len(k_map)
    if rows == 0:
        return []
    cols = len(k_map[0])
    groups = []

    for i1 in range(rows):
        for j1 in range(cols):
            if k_map[i1][j1] == 1:
                for i2 in range(i1, rows):
                    for j2 in range(j1, cols):
                        all_ones = True
                        for i in range(i1, i2 + 1):
                            for j in range(j1, j2 + 1):
                                if k_map[i % rows][j % cols] != 1:
                                    all_ones = False
                                    break
                            if not all_ones:
                                break

                        if all_ones:
                            group_size = (i2 - i1 + 1) * (j2 - j1 + 1)
                            if (group_size & (group_size - 1)) == 0:
                                groups.append((i1, j1, i2, j2))

    final_groups = []
    for group in groups:
        i1, j1, i2, j2 = group
        is_maximal = True
        for other in groups:
            oi1, oj1, oi2, oj2 = other
            if (i1 >= oi1 and j1 >= oj1 and i2 <= oi2 and j2 <= oj2 and
                    (i1 != oi1 or j1 != oj1 or i2 != oi2 or j2 != oj2)):
                is_maximal = False
                break
        if is_maximal:
            final_groups.append(group)

    return final_groups


def karnaugh_group_to_expression(
        group: Tuple[int, int, int, int],
        k_map: List[List[int]],
        variables: List[str],
        is_dnf: bool
) -> str:
    rows = len(k_map)
    cols = len(k_map[0]) if rows > 0 else 0
    num_vars = len(variables)
    i1, j1, i2, j2 = group

    def get_coordinates(num_bits):
        gray = []
        for x in range(1 << num_bits):
            gray.append(x ^ (x >> 1))
        return [format(g, f'0{num_bits}b') for g in gray]

    row_bits = num_vars // 2
    col_bits = (num_vars + 1) // 2
    row_gray = get_coordinates(row_bits)
    col_gray = get_coordinates(col_bits)

    positions = []
    for i in range(i1, i2 + 1):
        for j in range(j1, j2 + 1):
            bits = (row_gray[i % rows] + col_gray[j % cols])[:num_vars]
            positions.append(bits)

    if not positions:
        return "1" if is_dnf else "0"

    common = list(positions[0])
    for bits in positions[1:]:
        for idx, b in enumerate(bits):
            if common[idx] != b:
                common[idx] = '-'

    literals = []
    for idx, b in enumerate(common):
        if b == '-':
            continue
        var = variables[idx]
        if (b == '1' and is_dnf) or (b == '0' and not is_dnf):
            literals.append(var)
        else:
            literals.append(f"!{var}")

    if is_dnf:
        return " & ".join(literals) if literals else "1"
    else:
        return " | ".join(literals) if literals else "0"


def minimize_with_karnaugh_sdnf(minterms: List[int], num_vars: int) -> Tuple[str, List[List[str]]]:
    if not minterms:
        return "Always False", []

    variables = [chr(ord('a') + i) for i in range(num_vars)]
    k_map = build_karnaugh_map(minterms, num_vars)
    groups = find_karnaugh_groups(k_map)

    stages = [["Karnaugh map:"] + [" ".join(map(str, row)) for row in k_map]]
    stages.append(["Found groups:"] + [
        f"Group {i}: rows {i1}-{i2}, cols {j1}-{j2}" for i, (i1, j1, i2, j2) in enumerate(groups, 1)
    ])

    terms = []
    covered = set()

    for group in sorted(groups, key=lambda g: -(g[2] - g[0] + 1) * (g[3] - g[1] + 1)):
        group_cells = set()
        for i in range(group[0], group[2] + 1):
            for j in range(group[1], group[3] + 1):
                if k_map[i % len(k_map)][j % len(k_map[0])] == 1:
                    group_cells.add((i % len(k_map), j % len(k_map[0])))
        if not group_cells.issubset(covered):
            expr = karnaugh_group_to_expression(group, k_map, variables, is_dnf=True)
            terms.append(f"({expr})" if " & " in expr else expr)
            covered.update(group_cells)

    return " | ".join(terms) if terms else "Always False", stages


def minimize_with_karnaugh_sknf(maxterms: List[int], num_vars: int) -> Tuple[str, List[List[str]]]:
    if not maxterms:
        return "Always True", []

    variables = [chr(ord('a') + i) for i in range(num_vars)]
    minterms_sknf = [i for i in range(2 ** num_vars) if i not in maxterms]
    k_map = build_karnaugh_map(minterms_sknf, num_vars)
    inverted_map = [[1 - cell for cell in row] for row in k_map]

    groups = find_karnaugh_groups(inverted_map)

    cell_to_groups = {}
    group_cells_list = []

    for group in groups:
        i1, j1, i2, j2 = group
        group_cells = set()
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                i_wrapped = i % len(k_map)
                j_wrapped = j % len(k_map[0])
                if k_map[i_wrapped][j_wrapped] == 0:
                    cell = (i_wrapped, j_wrapped)
                    group_cells.add(cell)
                    cell_to_groups.setdefault(cell, set()).add(group)
        group_cells_list.append((group, group_cells))

    uncovered = set(cell_to_groups.keys())
    selected_groups = []

    while uncovered:
        best_group = None
        best_cover = set()
        for group, cells in group_cells_list:
            cover = cells & uncovered
            if len(cover) > len(best_cover):
                best_group = group
                best_cover = cover
        if not best_group:
            break
        selected_groups.append(best_group)
        uncovered -= best_cover

    stages = [["Karnaugh map (0s for CNF):"] + [" ".join(map(str, row)) for row in k_map]]
    stages.append(["Selected groups:"] + [
        f"Group {i}: rows {i1}-{i2}, cols {j1}-{j2}"
        for i, (i1, j1, i2, j2) in enumerate(selected_groups, 1)
    ])

    terms = []
    for group in selected_groups:
        expr = karnaugh_group_to_expression(group, k_map, variables, is_dnf=False)
        terms.append(f"({expr})" if " | " in expr else expr)

    return " & ".join(terms) if terms else "Always True", stages


def calculate_coverage_table(primes: List[Tuple[str, Set[int]]], minterms: Set[int]) -> Tuple[
    List[List[str]], List[Tuple[str, Set[int]]]]:
    coverage_table = []
    essential_primes = []

    table = []
    for pi in primes:
        row = []
        covered = pi[1].intersection(minterms)
        for m in sorted(minterms):
            row.append('X' if m in covered else '')
        table.append((pi[0], covered, row))

    remaining_minterms = set(minterms)
    for pi_pattern, covered, row in table:
        for m in covered:

            count = 0
            for other_pi, other_covered, _ in table:
                if m in other_covered:
                    count += 1
                    if count > 1:
                        break
            if count == 1:
                essential_primes.append((pi_pattern, covered))
                remaining_minterms -= covered
                break

    header = ["Implikant"] + [str(m) for m in sorted(minterms)]
    coverage_table.append(header)

    for pi_pattern, _, row in table:
        coverage_table.append([pi_pattern] + row)

    return coverage_table, essential_primes


def minimize_quine_mccluskey_sdnf(minterms: List[int], num_vars: int) -> Tuple[str, List[List[str]]]:
    if not minterms:
        return "Always False", []

    if len(minterms) == (1 << num_vars):
        return "Always True", [["All minterms are present (always True)"]]

    variables = [chr(ord('a') + i) for i in range(num_vars)]
    primes, combine_stages = find_prime_implicants(minterms, num_vars)

    unique_primes = []
    seen_patterns = set()
    for pattern, terms in primes:
        if pattern not in seen_patterns:
            seen_patterns.add(pattern)
            unique_primes.append((pattern, terms))

    minterm_set = set(minterms)
    coverage_table = []
    essential_primes = []
    remaining_minterms = set(minterms)

    header = ["Imp"] + [str(m) for m in sorted(minterms)]
    coverage_table.append(header)

    for pattern, terms in unique_primes:
        covered = terms & minterm_set
        row = [pattern] + ['X' if m in covered else '' for m in sorted(minterms)]
        coverage_table.append(row)

        for m in covered:
            count = sum(1 for _, t in unique_primes if m in t)
            if count == 1:
                essential_primes.append((pattern, covered))
                remaining_minterms -= covered
                break

    stages = []

    stage1 = ["Finding prime implicants:"]
    for stage in combine_stages:
        stage1.extend(stage)
    stages.append(stage1)

    stage2 = ["Coverage table:"] + [" ".join(row) for row in coverage_table]
    stages.append(stage2)

    stage3 = ["Essential prime implicants:"]
    if not essential_primes and remaining_minterms:
        for pattern, terms in unique_primes:
            covered = terms & remaining_minterms
            if covered:
                essential_primes.append((pattern, covered))
                remaining_minterms -= covered

    for pi in essential_primes:
        stage3.append(f"{pi[0]} covers {sorted(pi[1])}")
    stages.append(stage3)

    if not essential_primes and not minterms:
        return "Always False", stages

    terms = []
    for pi in essential_primes:
        term = pattern_to_expression(pi[0], variables, True)
        terms.append(f"({term})" if " & " in term else term)

    minimized = " | ".join(terms) if terms else "Always False"
    return minimized, stages


def minimize_quine_mccluskey_sknf(maxterms: List[int], num_vars: int) -> Tuple[str, List[List[str]]]:
    if not maxterms:
        return "Always True", []

    all_terms = set(range(1 << num_vars))
    if len(maxterms) == (1 << num_vars):
        return "Always False", [["All terms are maxterms (always False)"]]

    variables = [chr(ord('a') + i) for i in range(num_vars)]

    primes, combine_stages = find_prime_implicants(maxterms, num_vars)

    unique_primes = []
    seen = set()
    for pat, terms in primes:
        if pat not in seen:
            seen.add(pat)
            unique_primes.append((pat, terms))

    zero_terms = set(maxterms)
    coverage_rows = []
    header = ["Imp"] + [str(m) for m in sorted(zero_terms)]
    coverage_rows.append(header)

    essential = []
    remaining = set(zero_terms)

    for pat, terms in unique_primes:
        covered = terms & zero_terms
        row = [pat] + ['X' if m in covered else '' for m in sorted(zero_terms)]
        coverage_rows.append(row)
        for m in covered:
            cnt = sum(1 for _, t in unique_primes if m in t)
            if cnt == 1:
                essential.append((pat, covered))
                remaining -= covered
                break

    stages = []
    stages.append(["Finding prime implicates:"] + [step for sub in combine_stages for step in sub])
    stages.append(["Coverage table:"] + [" ".join(r) for r in coverage_rows])
    st3 = ["Essential prime implicates:"]
    if not essential and remaining:
        for pat, terms in unique_primes:
            cov = terms & remaining
            if cov:
                essential.append((pat, cov))
                remaining -= cov
    for pat, cov in essential:
        st3.append(f"{pat} covers {sorted(cov)}")
    stages.append(st3)

    if not essential:
        return "Always True", stages

    clauses = []
    for pat, _ in essential:
        clause = pattern_to_expression(pat, variables, is_dnf=False)
        if " | " in clause:
            clause = f"({clause})"
        clauses.append(clause)

    minimized = " & ".join(clauses)
    return minimized, stages