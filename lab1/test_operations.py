import unittest
from operations import (
    add_numbers, subtract_numbers, multiply_numbers, divide_numbers,
    float_to_ieee754, add_ieee754, ieee754_to_float,
    shift_left, binary_compare, add_numbers_binary
)
from binary_converter import (
    to_binary, to_complement, binary_to_decimal, fractional_to_binary,
    add_one, int_to_binary
)
from constants import BIT_SIZE, FRACTIONAL_PRECISION, IEEE754_SIZE, EXPONENT_SIZE, MANTISSA_SIZE, EXPONENT_OFFSET

class TestOperations(unittest.TestCase):
    def test_to_binary(self):
        """Тест преобразования в прямой код."""
        self.assertEqual(to_binary(3, BIT_SIZE), [0, 0, 0, 0, 1, 1])
        self.assertEqual(to_binary(-2, BIT_SIZE), [1, 0, 0, 0, 1, 0])
        self.assertEqual(to_binary(0, BIT_SIZE), [0, 0, 0, 0, 0, 0])
        self.assertEqual(to_binary(15, BIT_SIZE), [0, 0, 1, 1, 1, 1])  # Максимум
        self.assertEqual(to_binary(-16, BIT_SIZE), [1, 1, 0, 0, 0, 0])  # Минимум

    def test_to_complement(self):
        """Тест преобразования в дополнительный код."""
        self.assertEqual(to_complement([0, 0, 0, 0, 1, 1]), [0, 0, 0, 0, 1, 1])
        self.assertEqual(to_complement([1, 0, 0, 0, 1, 0]), [1, 1, 1, 1, 1, 0])
        self.assertEqual(to_complement([1, 0, 0, 0, 0, 0]), [1, 0, 0, 0, 0, 0])
        self.assertEqual(to_complement([1, 1, 0, 0, 0, 0]), [1, 1, 0, 0, 0, 0])  # -16
        self.assertEqual(to_complement([0, 0, 1, 1, 1, 1]), [0, 0, 1, 1, 1, 1])  # 15

    def test_binary_to_decimal(self):
        """Тест преобразования дополнительного кода в десятичное число."""
        self.assertEqual(binary_to_decimal([0, 0, 0, 0, 1, 1]), 3)
        self.assertEqual(binary_to_decimal([1, 1, 1, 1, 1, 0]), -2)
        self.assertEqual(binary_to_decimal([0, 0, 0, 0, 0, 0]), 0)
        self.assertEqual(binary_to_decimal([0, 0, 1, 1, 1, 1]), 15)
        self.assertEqual(binary_to_decimal([1, 1, 0, 0, 0, 0]), -16)

    def test_add_one(self):
        """Тест добавления единицы к двоичному числу."""
        self.assertEqual(add_one([1, 1, 1, 1, 0, 1]), [1, 1, 1, 1, 1, 0])
        self.assertEqual(add_one([0, 0, 0, 0, 0, 0]), [0, 0, 0, 0, 0, 1])
        self.assertEqual(add_one([0, 1, 1, 1, 1, 1]), [1, 0, 0, 0, 0, 0])
        self.assertEqual(add_one([1, 1, 1, 1, 1, 1]), [0, 0, 0, 0, 0, 0])  # Переполнение

    def test_int_to_binary(self):
        """Тест преобразования целого числа в двоичный список."""
        self.assertEqual(int_to_binary(3), [1, 1])
        self.assertEqual(int_to_binary(0), [0])
        self.assertEqual(int_to_binary(5), [1, 0, 1])
        self.assertEqual(int_to_binary(15), [1, 1, 1, 1])

    def test_fractional_to_binary(self):
        """Тест преобразования дробной части."""
        self.assertEqual(fractional_to_binary(0.5, 5), [1, 0, 0, 0, 0])
        self.assertEqual(fractional_to_binary(0.0, 5), [0, 0, 0, 0, 0])
        self.assertEqual(fractional_to_binary(0.75, 5), [1, 1, 0, 0, 0])
        self.assertEqual(fractional_to_binary(0.1, 5), [0, 0, 0, 1, 1])

    def test_add_numbers(self):
        """Тест сложения в дополнительном коде."""
        self.assertEqual(binary_to_decimal(add_numbers(3, -2)), 1)
        self.assertEqual(binary_to_decimal(add_numbers(0, 0)), 0)
        self.assertEqual(binary_to_decimal(add_numbers(-2, -2)), -4)
        self.assertEqual(binary_to_decimal(add_numbers(5, 3)), 8)
        self.assertEqual(binary_to_decimal(add_numbers(15, 1)), 16)  # Без обнуления при переполнении
        self.assertEqual(binary_to_decimal(add_numbers(-16, -1)), -17)  # Без обнуления при переполнении

    # def test_subtract_numbers(self):
    #     """Тест вычитания в дополнительном коде."""
    #     self.assertEqual(binary_to_decimal(subtract_numbers(3, -2)), 5)
    #     self.assertEqual(binary_to_decimal(subtract_numbers(3, 3)), 0)
    #     self.assertEqual(binary_to_decimal(subtract_numbers(-2, 2)), -4)
    #     self.assertEqual(binary_to_decimal(subtract_numbers(-3, -3)), 0)
    #     self.assertEqual(binary_to_decimal(subtract_numbers(5, 2)), 3)
    #     self.assertEqual(binary_to_decimal(subtract_numbers(15, -1)), 16)  # Без обнуления при переполнении
    #     self.assertEqual(binary_to_decimal(subtract_numbers(-16, 1)), -17)  # Без обнуления при переполнении

    def test_multiply_numbers(self):
        """Тест умножения в прямом коде."""
        self.assertEqual(binary_to_decimal(multiply_numbers(3, -2)), -6)
        self.assertEqual(binary_to_decimal(multiply_numbers(2, 2)), 4)
        self.assertEqual(binary_to_decimal(multiply_numbers(-3, -2)), 6)
        self.assertEqual(binary_to_decimal(multiply_numbers(0, 15)), 0)
        self.assertEqual(binary_to_decimal(multiply_numbers(5, 3)), 15)
        self.assertEqual(binary_to_decimal(multiply_numbers(-4, 4)), -16)

    def test_divide_numbers(self):
        """Тест деления в прямом коде."""
        int_code, frac_part = divide_numbers(3, -2)
        self.assertEqual(binary_to_decimal(int_code), -1)
        self.assertEqual(frac_part, [1, 0, 0, 0, 0])
        int_code, frac_part = divide_numbers(4, -2)
        self.assertEqual(binary_to_decimal(int_code), -2)
        self.assertEqual(frac_part, [0, 0, 0, 0, 0])
        int_code, frac_part = divide_numbers(-3, 2)
        self.assertEqual(binary_to_decimal(int_code), -1)
        self.assertEqual(frac_part, [1, 0, 0, 0, 0])
        int_code, frac_part = divide_numbers(1, 2)
        self.assertEqual(binary_to_decimal(int_code), 0)
        self.assertEqual(frac_part, [1, 0, 0, 0, 0])
        with self.assertRaises(ValueError):
            divide_numbers(3, 0)

    def test_shift_left(self):
        """Тест сдвига влево."""
        self.assertEqual(shift_left([0, 0, 0, 0, 1, 1], 0), [0, 0, 0, 1, 1, 0])
        self.assertEqual(shift_left([1, 1, 1, 1, 1, 1], 1), [1, 1, 1, 1, 1, 1])
        self.assertEqual(shift_left([0, 0, 0, 0, 0, 0], 1), [0, 0, 0, 0, 0, 1])
        self.assertEqual(shift_left([1, 0, 0, 0, 1, 0], 0), [0, 0, 0, 1, 0, 0])

    def test_binary_compare(self):
        """Тест сравнения двоичных чисел."""
        self.assertEqual(binary_compare([0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 0]), 1)
        self.assertEqual(binary_compare([0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0]), 0)
        self.assertEqual(binary_compare([0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1]), -1)
        self.assertEqual(binary_compare([1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 1, 1]), -1)  # -2 < 3
        self.assertEqual(binary_compare([0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0]), 1)  # 15 > -16

    def test_add_numbers_binary(self):
        """Тест двоичного сложения."""
        result = add_numbers_binary([0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 1, 0])
        self.assertEqual(binary_to_decimal(result), 1)  # 3 + (-2) = 1
        result = add_numbers_binary([0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0])
        self.assertEqual(binary_to_decimal(result), 0)  # 0 + 0 = 0
        result = add_numbers_binary([0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1])
        self.assertEqual(binary_to_decimal(result), 16)  # 15 + 1 = 16

    def test_float_to_ieee754(self):
        """Тест преобразования в IEEE-754."""
        result = float_to_ieee754(1.1)
        self.assertEqual(len(result), IEEE754_SIZE)
        self.assertEqual(result[:1], [0])
        self.assertEqual(float_to_ieee754(-1.1)[:1], [1])
        self.assertEqual(float_to_ieee754(0), [0] * IEEE754_SIZE)
        result = float_to_ieee754(0.0000001)
        self.assertEqual(result[0], 0)  # Денормализованное число
        result = float_to_ieee754(2**128)
        self.assertEqual(result[1:1+EXPONENT_SIZE], [1, 1, 1, 1, 1, 1, 1, 1])  # Бесконечность

    def test_add_ieee754(self):
        """Тест сложения в IEEE-754."""
        result = add_ieee754(1.1, 2.2)
        decimal_result = ieee754_to_float(result)
        self.assertAlmostEqual(decimal_result, 3.3, places=5)
        result = add_ieee754(-1.1, 2.2)
        decimal_result = ieee754_to_float(result)
        self.assertAlmostEqual(decimal_result, 1.1, places=5)
        result = add_ieee754(-1.1, -2.2)
        decimal_result = ieee754_to_float(result)
        self.assertAlmostEqual(decimal_result, -3.3, places=5)
        result = add_ieee754(0, 0)
        decimal_result = ieee754_to_float(result)
        self.assertEqual(decimal_result, 0.0)
        result = add_ieee754(2**127, 2**127)
        decimal_result = ieee754_to_float(result)
        self.assertAlmostEqual(decimal_result, 2**128, places=5)  # Без исключения для больших чисел
        result = add_ieee754(2**-128, -2**-128)
        decimal_result = ieee754_to_float(result)
        self.assertAlmostEqual(decimal_result, 0.0, places=5)

    def test_ieee754_to_float(self):
        """Тест преобразования IEEE-754 в число."""
        ieee_zero = [0] * IEEE754_SIZE
        self.assertEqual(ieee754_to_float(ieee_zero), 0.0)
        ieee_num = [0, 1, 0, 0, 0, 0, 0, 0, 0] + [0] * 23
        self.assertAlmostEqual(ieee754_to_float(ieee_num), 2.0, places=5)
        ieee_neg = [1, 1, 0, 0, 0, 0, 0, 0, 0] + [0] * 23
        self.assertAlmostEqual(ieee754_to_float(ieee_neg), -2.0, places=5)
        ieee_small = [0] + [0] * EXPONENT_SIZE + [1] + [0] * (MANTISSA_SIZE - 1)
        self.assertAlmostEqual(ieee754_to_float(ieee_small), 2**(-EXPONENT_OFFSET-1), places=5)

if __name__ == '__main__':
    unittest.main()