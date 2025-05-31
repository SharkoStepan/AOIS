from logic_engine import LogicalExpressionEvaluator

if __name__ == "__main__":
    expr = input("Введите логическое выражение (например, (a & !b) -> c): ")
    evaluator = LogicalExpressionEvaluator(expr)
    table = evaluator.generate_truth_table()
    evaluator.print_table(table)

    sdnf, sdnf_idx = evaluator.build_sdnf(table)
    print("\nСДНФ:")
    print(sdnf if sdnf else "Отсутствует")
    print(f"Числовая форма: {sdnf_idx}")

    sknf, sknf_idx = evaluator.build_sknf(table)
    print("\nСКНФ:")
    print(sknf if sknf else "Отсутствует")
    print(f"Числовая форма: {sknf_idx}")

    idx_form = [int(res) for _, res in table]
    print("\nИндексная форма функции:")
    print(f"F = ({''.join(map(str, idx_form))})")
