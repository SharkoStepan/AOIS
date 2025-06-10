from diagonal_matrix import DiagonalMatrix, MATRIX_SIZE


def main():
    # Пример матрицы
    example_matrix = [
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    matrix = DiagonalMatrix(example_matrix)

    # Вывод исходной матрицы
    matrix.print_matrix()

    # Чтение слова и столбца
    print("\nЧтение слова №0:", ''.join(map(str, matrix.read_word(0))))
    print("Чтение столбца №3:", ''.join(map(str, matrix.read_column(3))))

    # Логические функции
    result_f0 = matrix.logical_function(0, 1, 0)
    print("Результат f0 (слова 0 и 1):", ''.join(map(str, result_f0)))

    result_f5 = matrix.logical_function(0, 1, 5)
    print("Результат f5 (слова 0 и 1):", ''.join(map(str, result_f5)))
    matrix.write_word(15, result_f5)

    result_f10 = matrix.logical_function(0, 1, 10)
    print("Результат f10 (слова 0 и 1):", ''.join(map(str, result_f10)))

    result_f15 = matrix.logical_function(0, 1, 15)
    print("Результат f15 (слова 0 и 1):", ''.join(map(str, result_f15)))

    # Поиск по ключу и сложение полей
    key = "111"
    matching_words = matrix.search_by_key(key)
    print(f"\nСлова с ключом {key}:", matching_words)
    for word_index in matching_words:
        matrix.add_fields(word_index, key)

    # Поиск по соответствию
    search_arg = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print("\nПоиск по соответствию (аргумент:", ''.join(map(str, search_arg)), ")")
    for j in range(MATRIX_SIZE):
        g, l = matrix.compute_gl(search_arg, j)
        print(f"Слово {j}: g={g[0]}, l={l[0]}, совпадений: {matrix.match_count(search_arg, j)}")

    best_matches = matrix.search_by_correspondence(search_arg)
    print("Слова с максимальным количеством совпадений:", best_matches)

    # Вывод матрицы после операций
    print("\nМатрица после операций:")
    matrix.print_matrix()


if __name__ == "__main__":
    main()