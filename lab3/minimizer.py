def print_stage(stage_num, description, implicants):
    print(f"\nЭтап {stage_num}: {description}")
    for i, imp in enumerate(implicants, 1): print(f"{i}. {imp}")

def get_minterms(variables, table, value):
    return [[(v, val) for v, val in zip(variables, row[:-1])] for row in table if row[-1] == value]

def term_to_string(term, is_sdnf):
    if not term: return "0" if is_sdnf else "1"
    parts = [var if val == (1 if is_sdnf else 0) else f"¬{var}" for var, val in term]
    return ("∧" if is_sdnf else "∨").join(parts)

def can_glue(t1, t2):
    diff, diff_pos = 0, -1
    for i, (v1, v2) in enumerate(zip(t1, t2)):
        if v1[1] != v2[1]:
            diff += 1
            diff_pos = i
        if diff > 1: return False, -1
    return diff == 1, diff_pos

def glue_terms(t1, t2, pos):
    return [(v, val) for i, (v, val) in enumerate(t1) if i != pos]

def build_coverage_table(terms, minterms):
    if not minterms: return [[0] * len(terms)]
    table = [[0] * len(minterms) for _ in range(len(terms))]
    for i, term in enumerate(terms):
        term_dict = dict(term)
        for j, minterm in enumerate(minterms):
            table[i][j] = 1 if all(v not in term_dict or term_dict[v] == val for v, val in minterm) else 0
    return table

def select_essential_implicants(terms, minterms):
    if not minterms or not terms: return []
    coverage_table = build_coverage_table(terms, minterms)
    selected, covered = [], set()
    for j in range(len(minterms)):
        covering = [i for i in range(len(terms)) if coverage_table[i][j] == 1]
        if len(covering) == 1 and covering[0] not in selected:
            selected.append(covering[0])
            covered.add(j)
    remaining = set(range(len(minterms))) - covered
    while remaining:
        best_term, best_cover = None, 0
        for i in range(len(terms)):
            if i in selected: continue
            cover = sum(1 for j in remaining if coverage_table[i][j] == 1)
            if cover > best_cover:
                best_cover, best_term = cover, i
        if best_term is not None:
            selected.append(best_term)
            covered.update(j for j in range(len(minterms)) if coverage_table[best_term][j] == 1)
            remaining = set(range(len(minterms))) - covered
        else: break
    return [terms[i] for i in sorted(set(selected))]

def minimize_sdnf_calc_method(variables, table):
    if not variables: return str(table[0][0])
    terms = get_minterms(variables, table, 1)
    if not terms: return "0"
    print_stage(1, "Исходные минтермы", [term_to_string(t, True) for t in terms])
    stage, all_terms = 2, terms.copy()
    while True:
        new_terms, used = [], set()
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                can, pos = can_glue(terms[i], terms[j])
                if can:
                    new_term = glue_terms(terms[i], terms[j], pos)
                    if new_term not in new_terms:
                        new_terms.append(new_term)
                    used.add(i)
                    used.add(j)
        if not new_terms: break
        all_terms.extend(new_terms)
        terms = [t for i, t in enumerate(terms) if i not in used] + new_terms
        print_stage(stage, f"Импликанты после склеивания (этап {stage - 1})", [term_to_string(t, True) for t in terms])
        stage += 1
    selected = select_essential_implicants(all_terms, get_minterms(variables, table, 1))
    print_stage(stage, "Результат минимизации", [term_to_string(t, True) for t in selected])
    return " ∨ ".join(f"({term_to_string(t, True)})" for t in selected) or "0"

def minimize_sknf_calc_method(variables, table):
    if not variables: return str(table[0][0])
    terms = get_minterms(variables, table, 0)
    if not terms: return "1"
    print_stage(1, "Исходные макстермы", [term_to_string(t, False) for t in terms])
    stage, all_terms = 2, terms.copy()
    while True:
        new_terms, used = [], set()
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                can, pos = can_glue(terms[i], terms[j])
                if can:
                    new_term = glue_terms(terms[i], terms[j], pos)
                    if new_term not in new_terms:
                        new_terms.append(new_term)
                    used.add(i)
                    used.add(j)
        if not new_terms: break
        all_terms.extend(new_terms)
        terms = [t for i, t in enumerate(terms) if i not in used] + new_terms
        print_stage(stage, f"Импликанты после склеивания (этап {stage - 1})", [term_to_string(t, False) for t in terms])
        stage += 1
    selected = select_essential_implicants(all_terms, get_minterms(variables, table, 0))
    print_stage(stage, "Результат минимизации", [term_to_string(t, False) for t in selected])
    return " ∧ ".join(f"({term_to_string(t, False)})" for t in selected) or "1"

def print_coverage_table(terms, minterms, table, is_sdnf):
    print("\nТаблица покрытия:")
    header = " | ".join([term_to_string(m, is_sdnf) for m in minterms])
    print(" " * 15 + header)
    print("-" * (15 + len(header)))
    for i, term in enumerate(terms):
        print(f"{term_to_string(term, is_sdnf):<15} | {' | '.join(map(str, table[i]))}")

def minimize_sdnf_table_method(variables, table):
    if not variables: return str(table[0][0])
    terms = get_minterms(variables, table, 1)
    if not terms: return "0"
    print_stage(1, "Исходные минтермы", [term_to_string(t, True) for t in terms])
    stage, all_terms = 2, terms.copy()
    while True:
        new_terms, used = [], set()
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                can, pos = can_glue(terms[i], terms[j])
                if can:
                    new_term = glue_terms(terms[i], terms[j], pos)
                    if new_term not in new_terms:
                        new_terms.append(new_term)
                    used.add(i)
                    used.add(j)
        if not new_terms: break
        all_terms.extend(new_terms)
        terms = [t for i, t in enumerate(terms) if i not in used] + new_terms
        print_stage(stage, f"Импликанты после склеивания (этап {stage - 1})", [term_to_string(t, True) for t in terms])
        stage += 1
    minterms = get_minterms(variables, table, 1)
    coverage_table = build_coverage_table(all_terms, minterms)
    print_coverage_table(all_terms, minterms, coverage_table, True)
    selected = select_essential_implicants(all_terms, minterms)
    print_stage(stage, "Результат минимизации", [term_to_string(t, True) for t in selected])
    return " ∨ ".join(f"({term_to_string(t, True)})" for t in selected) or "0"

def minimize_sknf_table_method(variables, table):
    if not variables: return str(table[0][0])
    terms = get_minterms(variables, table, 0)
    if not terms: return "1"
    print_stage(1, "Исходные макстермы", [term_to_string(t, False) for t in terms])
    stage, all_terms = 2, terms.copy()
    while True:
        new_terms, used = [], set()
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                can, pos = can_glue(terms[i], terms[j])
                if can:
                    new_term = glue_terms(terms[i], terms[j], pos)
                    if new_term not in new_terms:
                        new_terms.append(new_term)
                    used.add(i)
                    used.add(j)
        if not new_terms: break
        all_terms.extend(new_terms)
        terms = [t for i, t in enumerate(terms) if i not in used] + new_terms
        print_stage(stage, f"Импликанты после склеивания (этап {stage - 1})", [term_to_string(t, False) for t in terms])
        stage += 1
    minterms = get_minterms(variables, table, 0)
    coverage_table = build_coverage_table(all_terms, minterms)
    print_coverage_table(all_terms, minterms, coverage_table, False)
    selected = select_essential_implicants(all_terms, minterms)
    print_stage(stage, "Результат минимизации", [term_to_string(t, False) for t in selected])
    return " ∧ ".join(f"({term_to_string(t, False)})" for t in selected) or "1"

def minimize_sdnf_kmap_method(variables, table):
    from karnaugh_map import minimize_sdnf_kmap
    return minimize_sdnf_kmap(variables, table)

def minimize_sknf_kmap_method(variables, table):
    from karnaugh_map import minimize_sknf_kmap
    return minimize_sknf_kmap(variables, table)