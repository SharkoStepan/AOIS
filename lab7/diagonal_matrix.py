from typing import List, Tuple

# Глобальные константы
MATRIX_SIZE = 16
WORD_LENGTH = 16
KEY_LENGTH = 3
FIELD_A_LENGTH = 4
FIELD_B_LENGTH = 4
FIELD_S_LENGTH = 5
VALID_KEYS = [format(i, '03b') for i in range(8)]  # 000-111


class DiagonalMatrix:
    """Класс для работы с матрицей 16x16 с диагональной адресацией."""

    def __init__(self, matrix: List[List[int]]):
        """Инициализация матрицы."""
        if len(matrix) != MATRIX_SIZE or any(len(row) != MATRIX_SIZE for row in matrix):
            raise ValueError("Матрица должна быть 16x16")
        self.matrix = [row[:] for row in matrix]  # Глубокая копия

    def read_word(self, word_index: int) -> List[int]:
        """Чтение слова по индексу с учетом диагональной адресации."""
        if not 0 <= word_index < MATRIX_SIZE:
            raise ValueError("Недопустимый индекс слова")
        word = []
        for i in range(WORD_LENGTH):
            col = (word_index + i) % MATRIX_SIZE
            word.append(self.matrix[i][col])
        return word

    def read_column(self, col_index: int) -> List[int]:
        """Чтение разрядного столбца по индексу."""
        if not 0 <= col_index < MATRIX_SIZE:
            raise ValueError("Недопустимый индекс столбца")
        return [self.matrix[i][col_index] for i in range(MATRIX_SIZE)]

    def write_word(self, word_index: int, word: List[int]) -> None:
        """Запись слова в матрицу с учетом диагональной адресации."""
        if len(word) != WORD_LENGTH:
            raise ValueError("Длина слова должна быть 16 бит")
        for i in range(WORD_LENGTH):
            col = (word_index + i) % MATRIX_SIZE
            self.matrix[i][col] = word[i]

    def logical_function(self, word_index1: int, word_index2: int, func_id: int) -> List[int]:
        """Выполнение логической функции над двумя словами."""
        word1 = self.read_word(word_index1)
        word2 = self.read_word(word_index2)
        if func_id == 0:  # A AND B
            return [a & b for a, b in zip(word1, word2)]
        elif func_id == 5:  # A OR NOT B
            return [a | (1 - b) for a, b in zip(word1, word2)]
        elif func_id == 10:  # NOT A OR B
            return [(1 - a) | b for a, b in zip(word1, word2)]
        elif func_id == 15:  # A OR B
            return [a | b for a, b in zip(word1, word2)]
        raise ValueError("Недопустимый идентификатор функции")

    def compute_gl(self, search_arg: List[int], word_index: int) -> Tuple[List[int], List[int]]:
        """Вычисление g_ji и l_ji для слова по рекуррентным формулам."""
        word = self.read_word(word_index)
        g = [0] * (WORD_LENGTH + 1)
        l = [0] * (WORD_LENGTH + 1)
        g[WORD_LENGTH] = l[WORD_LENGTH] = 0  # Начальные условия

        for i in range(WORD_LENGTH - 1, -1, -1):
            g[i] = g[i + 1] and ((not search_arg[i]) and word[i] and (not l[i + 1]))
            l[i] = l[i + 1] or (search_arg[i] and (not word[i]) and (not g[i + 1]))

        return g, l

    def match_count(self, search_arg: List[int], word_index: int) -> int:
        """Подсчет совпадающих разрядов для поиска по соответствию."""
        word = self.read_word(word_index)
        return sum(1 for a, s in zip(search_arg, word) if a == s)

    def search_by_correspondence(self, search_arg: List[int]) -> List[Tuple[int, int]]:
        """Поиск слов с максимальным количеством совпадающих разрядов."""
        matches = []
        max_count = 0
        for j in range(MATRIX_SIZE):
            count = self.match_count(search_arg, j)
            matches.append((j, count))
            max_count = max(max_count, count)

        return [match for match in matches if match[1] == max_count]

    def search_by_key(self, key: str) -> List[int]:
        """Поиск слов, у которых первые 3 бита совпадают с ключом."""
        if key not in VALID_KEYS:
            raise ValueError("Ключ должен быть от 000 до 111")
        return [j for j in range(MATRIX_SIZE) if ''.join(map(str, self.read_word(j)[:KEY_LENGTH])) == key]

    def add_fields(self, word_index: int, key: str) -> None:
        """Сложение полей A и B в слове, если V совпадает с ключом."""
        word = self.read_word(word_index)
        word_key = ''.join(map(str, word[:KEY_LENGTH]))
        if word_key != key:
            return

        field_a = word[KEY_LENGTH:KEY_LENGTH + FIELD_A_LENGTH]
        field_b = word[KEY_LENGTH + FIELD_A_LENGTH:KEY_LENGTH + FIELD_A_LENGTH + FIELD_B_LENGTH]

        a_value = int(''.join(map(str, field_a)), 2)
        b_value = int(''.join(map(str, field_b)), 2)
        sum_value = a_value + b_value

        if sum_value >= 2 ** FIELD_S_LENGTH:
            sum_value %= 2 ** FIELD_S_LENGTH

        sum_bits = list(map(int, format(sum_value, f'0{FIELD_S_LENGTH}b')))
        word[
        KEY_LENGTH + FIELD_A_LENGTH + FIELD_B_LENGTH:KEY_LENGTH + FIELD_A_LENGTH + FIELD_B_LENGTH + FIELD_S_LENGTH] = sum_bits
        self.write_word(word_index, word)

    def print_matrix(self) -> None:
        """Вывод матрицы в консоль."""
        print("Матрица 16x16:")
        for row in self.matrix:
            print(' '.join(map(str, row)))