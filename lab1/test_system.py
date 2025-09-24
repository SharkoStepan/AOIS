import unittest
from numerical_representations import *
from arithmetic_processor import *


class TestNumericalSystem(unittest.TestCase):
    def setUp(self):
        self.converter = BinaryConverter()

    def test_binary_conversion_positive(self):
        """Тестирование преобразования положительных чисел"""
        self.assertEqual(integer_to_binary_string(5), "0000000000000101")
        self.assertEqual(integer_to_binary_string(10), "0000000000001010")
        self.assertEqual(integer_to_binary_string(255), "0000000011111111")
        self.assertEqual(integer_to_binary_string(0), "0000000000000000")

    def test_binary_conversion_negative(self):
        """Тестирование преобразования отрицательных чисел"""
        self.assertEqual(integer_to_binary_string(-5), "1111111111111011")
        self.assertEqual(integer_to_binary_string(-10), "1111111111110110")
        self.assertEqual(integer_to_binary_string(-1), "1111111111111111")

    def test_binary_to_integer_conversion(self):
        """Тестирование обратного преобразования"""
        self.assertEqual(binary_string_to_integer("0000000000000101"), 5)
        self.assertEqual(binary_string_to_integer("1111111111111011"), -5)
        self.assertEqual(binary_string_to_integer("0000000000000000"), 0)
        self.assertEqual(binary_string_to_integer("0111111111111111"), 32767)
        self.assertEqual(binary_string_to_integer("1000000000000000"), -32768)

    def test_arithmetic_addition(self):
        """Тестирование сложения"""
        bin_result, dec_result = addition_with_binary(5, 3)
        self.assertEqual(dec_result, 8)
        # Исправлено: ожидаем правильный формат
        self.assertEqual(bin_result, "1000")  # 8 в двоичной

        bin_result, dec_result = addition_with_binary(-5, -3)
        self.assertEqual(dec_result, -8)

        bin_result, dec_result = addition_with_binary(5, -3)
        self.assertEqual(dec_result, 2)

    def test_arithmetic_subtraction(self):
        """Тестирование вычитания"""
        bin_result, dec_result = subtraction_with_binary(10, 4)
        self.assertEqual(dec_result, 6)
        self.assertEqual(bin_result, "110")  # 6 в двоичной

        bin_result, dec_result = subtraction_with_binary(-5, -3)
        self.assertEqual(dec_result, -2)

        bin_result, dec_result = subtraction_with_binary(5, -3)
        self.assertEqual(dec_result, 8)

    def test_arithmetic_multiplication(self):
        """Тестирование умножения"""
        bin_result, dec_result = multiplication_with_binary(5, 3)
        self.assertEqual(dec_result, 15)
        self.assertEqual(bin_result, "1111")  # 15 в двоичной

        bin_result, dec_result = multiplication_with_binary(-5, 3)
        self.assertEqual(dec_result, -15)

        bin_result, dec_result = multiplication_with_binary(5, -3)
        self.assertEqual(dec_result, -15)

    def test_arithmetic_division(self):
        """Тестирование деления"""
        bin_result, dec_result = division_with_binary(10, 2)
        self.assertAlmostEqual(dec_result, 5.0, places=5)
        self.assertTrue("101" in bin_result)

        bin_result, dec_result = division_with_binary(-10, 2)
        self.assertAlmostEqual(dec_result, -5.0, places=5)

        bin_result, dec_result = division_with_binary(10, 3)
        self.assertAlmostEqual(dec_result, 3.3125, places=5)

    def test_division_by_zero(self):
        """Тестирование деления на ноль"""
        bin_result, dec_result = division_with_binary(10, 0)
        self.assertEqual(bin_result, "ERROR")
        self.assertEqual(dec_result, "Деление на ноль")

    def test_ieee754_conversion(self):
        """Тестирование IEEE754 преобразований"""
        test_cases = [0.0, 1.0, -1.0, 2.5, -3.75, 0.125, 10.5, -15.75]

        for value in test_cases:
            with self.subTest(value=value):
                bits = ieee754_representation(value)
                reconstructed = ieee754_to_float(bits)
                self.assertAlmostEqual(value, reconstructed, places=6)

    def test_ieee754_specific_values(self):
        """Тестирование конкретных IEEE754 значений"""
        bits = ieee754_representation(0.0)
        self.assertEqual(ieee754_to_float(bits), 0.0)

        bits = ieee754_representation(1.0)
        self.assertAlmostEqual(ieee754_to_float(bits), 1.0, places=6)

        bits = ieee754_representation(-2.5)
        self.assertAlmostEqual(ieee754_to_float(bits), -2.5, places=6)


class TestRepresentations(unittest.TestCase):
    def test_direct_code(self):
        """Тестирование прямого кода"""
        self.assertEqual(direct_code_representation(5), "0000000000000101")
        self.assertEqual(direct_code_representation(-5), "1000000000000101")
        self.assertEqual(direct_code_representation(0), "0000000000000000")

    def test_ones_complement(self):
        """Тестирование обратного кода"""
        self.assertEqual(ones_complement_representation(5), "0000000000000101")
        self.assertEqual(ones_complement_representation(-5), "1111111111111010")
        self.assertEqual(ones_complement_representation(0), "0000000000000000")

    def test_twos_complement(self):
        """Тестирование дополнительного кода"""
        self.assertEqual(complement_representation(5), "0000000000000101")
        self.assertEqual(complement_representation(-5), "1111111111111011")
        self.assertEqual(complement_representation(0), "0000000000000000")


class TestBinaryOperations(unittest.TestCase):
    def test_binary_addition(self):
        """Тестирование двоичного сложения"""
        result = binary_addition("1010", "1100")
        self.assertEqual(result, "10110")  # 10 + 12 = 22

        result = binary_addition("1111", "0001")
        self.assertEqual(result, "10000")  # 15 + 1 = 16

        result = binary_addition("0000", "0000")
        self.assertEqual(result, "0")  # 0 + 0 = 0

    def test_binary_addition_different_lengths(self):
        """Тестирование сложения строк разной длины"""
        result = binary_addition("1", "111")
        self.assertEqual(result, "1000")  # 1 + 7 = 8

        result = binary_addition("101", "1")
        self.assertEqual(result, "110")  # 5 + 1 = 6

    def test_edge_cases(self):
        """Тестирование граничных случаев"""
        # Нули
        result = binary_addition("0000", "0000")
        self.assertEqual(result, "0")

        # Преобразование туда-обратно для положительных чисел
        original = 123
        binary = integer_to_binary_string(original)
        restored = binary_string_to_integer(binary)
        self.assertEqual(original, restored)

        # Преобразование туда-обратно для отрицательных чисел
        original = -45
        binary = integer_to_binary_string(original)
        restored = binary_string_to_integer(binary)
        self.assertEqual(original, restored)

        # Граничные значения 16-битных чисел
        self.assertEqual(binary_string_to_integer("0111111111111111"), 32767)
        self.assertEqual(binary_string_to_integer("1000000000000000"), -32768)


class TestFloatOperations(unittest.TestCase):
    def test_float_addition(self):
        """Тестирование сложения с плавающей точкой"""
        result_bits, result_value = floating_point_addition_with_bits(1.5, 2.5)
        self.assertAlmostEqual(result_value, 4.0, places=6)

        result_bits, result_value = floating_point_addition_with_bits(-1.5, 2.5)
        self.assertAlmostEqual(result_value, 1.0, places=6)

        result_bits, result_value = floating_point_addition_with_bits(0.0, 0.0)
        self.assertAlmostEqual(result_value, 0.0, places=6)


class TestConverterClasses(unittest.TestCase):
    def test_binary_converter_class(self):
        """Тестирование класса BinaryConverter"""
        converter = BinaryConverter()

        # Тест to_binary
        self.assertEqual(converter.to_binary(5), "0000000000000101")
        self.assertEqual(converter.to_binary(-5), "1111111111111011")

        # Тест from_binary
        self.assertEqual(converter.from_binary("0000000000000101"), 5)
        self.assertEqual(converter.from_binary("1111111111111011"), -5)

        # Тест ones_complement
        self.assertEqual(converter.ones_complement(5), "0000000000000101")
        self.assertEqual(converter.ones_complement(-5), "1111111111111010")

        # Тест signed_magnitude
        self.assertEqual(converter.signed_magnitude(5), "0000000000000101")
        self.assertEqual(converter.signed_magnitude(-5), "1000000000000101")

    def test_ieee754_converter_class(self):
        """Тестирование класса IEEE754Converter"""
        converter = IEEE754Converter()

        # Тест float_to_bits
        bits = converter.float_to_bits(1.0)
        self.assertEqual(len(bits), 32)

        # Тест bits_to_float
        value = converter.bits_to_float(bits)
        self.assertAlmostEqual(value, 1.0, places=6)

        # Тест для нуля
        bits_zero = converter.float_to_bits(0.0)
        value_zero = converter.bits_to_float(bits_zero)
        self.assertEqual(value_zero, 0.0)


def test_binary_operations_comprehensive():
    """Комплексное тестирование бинарных операций"""
    print("Комплексное тестирование бинарных операций...")

    # Тестирование различных комбинаций
    test_pairs = [
        (0, 0),
        (1, 1),
        (5, 3),
        (10, 15),
        (127, 128),
        (-5, -3),
        (5, -3)
    ]

    for a, b in test_pairs:
        # Сложение
        bin_res, dec_res = addition_with_binary(a, b)
        assert dec_res == a + b, f"Ошибка сложения: {a} + {b}"

        # Вычитание
        bin_res, dec_res = subtraction_with_binary(a, b)
        assert dec_res == a - b, f"Ошибка вычитания: {a} - {b}"

        # Умножение
        bin_res, dec_res = multiplication_with_binary(a, b)
        assert dec_res == a * b, f"Ошибка умножения: {a} * {b}"

    print("Все комплексные тесты пройдены!")


if __name__ == "__main__":
    # Запуск комплексного тестирования
    test_binary_operations_comprehensive()

    print("\n" + "=" * 60)
    print("ЗАПУСК UNIT-ТЕСТОВ")
    print("=" * 60)

    # Запуск unit-тестов
    unittest.main(verbosity=2)