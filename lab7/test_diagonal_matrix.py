import unittest
from typing import List
from diagonal_matrix import DiagonalMatrix, MATRIX_SIZE, WORD_LENGTH, KEY_LENGTH, FIELD_A_LENGTH, FIELD_B_LENGTH, FIELD_S_LENGTH, VALID_KEYS

class TestDiagonalMatrix(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой матрицы 16x16."""
        self.test_matrix = [
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
        self.matrix = DiagonalMatrix(self.test_matrix)

    def test_init_valid_matrix(self):
        """Проверка корректной инициализации матрицы."""
        self.assertEqual(len(self.matrix.matrix), MATRIX_SIZE)
        self.assertEqual(len(self.matrix.matrix[0]), MATRIX_SIZE)
        self.assertEqual(self.matrix.matrix, self.test_matrix)

    def test_init_invalid_matrix(self):
        """Проверка обработки некорректной матрицы."""
        invalid_matrix = [[0] * MATRIX_SIZE] * (MATRIX_SIZE - 1)
        with self.assertRaises(ValueError):
            DiagonalMatrix(invalid_matrix)
        invalid_matrix = [[0] * (MATRIX_SIZE - 1)] * MATRIX_SIZE
        with self.assertRaises(ValueError):
            DiagonalMatrix(invalid_matrix)

    def test_read_word(self):
        """Проверка чтения слова с диагональной адресацией."""
        word = self.matrix.read_word(0)
        self.assertEqual(len(word), WORD_LENGTH)
        self.assertTrue(all(bit in [0, 1] for bit in word))

    def test_read_word_invalid_index(self):
        """Проверка обработки некорректного индекса слова."""
        with self.assertRaises(ValueError):
            self.matrix.read_word(-1)
        with self.assertRaises(ValueError):
            self.matrix.read_word(MATRIX_SIZE)

    def test_read_column(self):
        """Проверка чтения столбца."""
        column = self.matrix.read_column(3)
        expected = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(column, expected)
        self.assertEqual(len(column), MATRIX_SIZE)

    def test_read_column_invalid_index(self):
        """Проверка обработки некорректного индекса столбца."""
        with self.assertRaises(ValueError):
            self.matrix.read_column(-1)
        with self.assertRaises(ValueError):
            self.matrix.read_column(MATRIX_SIZE)

    def test_write_word(self):
        """Проверка записи слова."""
        new_word = [1] * WORD_LENGTH
        self.matrix.write_word(0, new_word)
        read_word = self.matrix.read_word(0)
        self.assertEqual(read_word, new_word)

    def test_write_word_invalid_length(self):
        """Проверка обработки некорректной длины слова."""
        with self.assertRaises(ValueError):
            self.matrix.write_word(0, [0] * (WORD_LENGTH - 1))

    def test_logical_function_f0(self):
        """Проверка логической функции f0 (AND) с нулевыми словами."""
        self.matrix.write_word(0, [0] * WORD_LENGTH)
        self.matrix.write_word(1, [0] * WORD_LENGTH)
        result = self.matrix.logical_function(0, 1, 0)
        self.assertEqual(result, [0] * WORD_LENGTH)

    def test_logical_function_f5(self):
        """Проверка логической функции f5 (A OR NOT B) с нулевыми словами."""
        self.matrix.write_word(0, [0] * WORD_LENGTH)
        self.matrix.write_word(1, [0] * WORD_LENGTH)
        result = self.matrix.logical_function(0, 1, 5)
        self.assertEqual(result, [1] * WORD_LENGTH)

    def test_logical_function_f10(self):
        """Проверка логической функции f10 (NOT A OR B) с нулевыми словами."""
        self.matrix.write_word(0, [0] * WORD_LENGTH)
        self.matrix.write_word(1, [0] * WORD_LENGTH)
        result = self.matrix.logical_function(0, 1, 10)
        self.assertEqual(result, [1] * WORD_LENGTH)

    def test_logical_function_f15(self):
        """Проверка логической функции f15 (OR) с нулевыми словами."""
        self.matrix.write_word(0, [0] * WORD_LENGTH)
        self.matrix.write_word(1, [0] * WORD_LENGTH)
        result = self.matrix.logical_function(0, 1, 15)
        self.assertEqual(result, [0] * WORD_LENGTH)

    def test_logical_function_invalid_id(self):
        """Проверка обработки некорректного ID функции."""
        with self.assertRaises(ValueError):
            self.matrix.logical_function(0, 1, 999)

    def test_compute_gl(self):
        """Проверка вычисления g и l для одинаковых слов."""
        self.matrix.write_word(0, [0] * WORD_LENGTH)
        g, l = self.matrix.compute_gl([0] * WORD_LENGTH, 0)
        self.assertEqual(g[0], 0)
        self.assertEqual(l[0], 0)

    def test_match_count(self):
        """Проверка подсчета совпадений для одинаковых слов."""
        self.matrix.write_word(0, [0] * WORD_LENGTH)
        count = self.matrix.match_count([0] * WORD_LENGTH, 0)
        self.assertEqual(count, WORD_LENGTH)

    def test_search_by_correspondence(self):
        """Проверка поиска по соответствию для нулевого аргумента."""
        self.matrix.write_word(0, [0] * WORD_LENGTH)
        matches = self.matrix.search_by_correspondence([0] * WORD_LENGTH)
        self.assertTrue(any(idx == 0 and count == WORD_LENGTH for idx, count in matches))

    def test_search_by_key(self):
        """Проверка поиска по ключу '000'."""
        self.matrix.write_word(0, [0, 0, 0] + [0] * (WORD_LENGTH - KEY_LENGTH))
        matches = self.matrix.search_by_key("000")
        self.assertTrue(0 in matches)

    def test_search_by_key_invalid(self):
        """Проверка обработки некорректного ключа."""
        with self.assertRaises(ValueError):
            self.matrix.search_by_key("999")

    def test_add_fields(self):
        """Проверка сложения полей A и B для ключа '000'."""
        word = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # V=000, A=0000, B=0000, S=00000
        self.matrix.write_word(0, word)
        self.matrix.add_fields(0, "000")
        read_word = self.matrix.read_word(0)
        expected_s = [0, 0, 0, 0, 0]  # A(0) + B(0) = 0
        self.assertEqual(read_word[KEY_LENGTH + FIELD_A_LENGTH + FIELD_B_LENGTH:], expected_s)

    def test_add_fields_no_match(self):
        """Проверка, что слово не изменяется, если ключ не совпадает."""
        original_word = self.matrix.read_word(1)
        self.matrix.add_fields(1, "111")
        self.assertEqual(self.matrix.read_word(1), original_word)

    def test_print_matrix(self):
        """Проверка вывода матрицы (захват вывода в консоль)."""
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        self.matrix.print_matrix()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertTrue(output.startswith("Матрица 16x16:"))
        self.assertEqual(len(output.splitlines()) - 1, MATRIX_SIZE)

if __name__ == "__main__":
    unittest.main()