import unittest
from num_converters import *
from num_operations import *

class TestNumConverters(unittest.TestCase):
    def test_num_to_binary(self):
        self.assertEqual(num_to_binary(0), "0")
        self.assertEqual(num_to_binary(5), "101")
        self.assertEqual(num_to_binary(10), "1010")
        self.assertEqual(num_to_binary(255), "11111111")

    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal("0"), 0)
        self.assertEqual(binary_to_decimal("101"), 5)
        self.assertEqual(binary_to_decimal("1010"), 10)
        self.assertEqual(binary_to_decimal("11111111"), 255)

    def test_num_to_signed_magnitude(self):
        self.assertEqual(num_to_signed_magnitude(5), "0000000000000101")
        self.assertEqual(num_to_signed_magnitude(-5), "1000000000000101")
        self.assertEqual(num_to_signed_magnitude(0), "0000000000000000")

    def test_num_to_ones_complement(self):
        self.assertEqual(num_to_ones_complement(5), "0000000000000101")
        self.assertEqual(num_to_ones_complement(-5), "1111111111111010")
        self.assertEqual(num_to_ones_complement(0), "0000000000000000")

    def test_num_to_twos_complement(self):
        self.assertEqual(num_to_twos_complement(5), "0000000000000101")
        self.assertEqual(num_to_twos_complement(-5), "1111111111111011")
        self.assertEqual(num_to_twos_complement(0), "0000000000000000")

    def test_binary_to_decimal_twos(self):
        self.assertEqual(binary_to_decimal_twos("00000101"), 5)
        self.assertEqual(binary_to_decimal_twos("11111011"), -5)
        self.assertEqual(binary_to_decimal_twos("00000000"), 0)

    def test_num_to_ieee754(self):
        self.assertEqual(num_to_ieee754(0), IEEE754_NULL)
        self.assertEqual(num_to_ieee754(1.0), "00111111100000000000000000000000")
        self.assertEqual(num_to_ieee754(-2.5), "11000000001000000000000000000000")

    def test_ieee754_to_num(self):
        self.assertEqual(ieee754_to_num(IEEE754_NULL), 0.0)
        self.assertEqual(ieee754_to_num("00111111100000000000000000000000"), 1.0)
        self.assertEqual(ieee754_to_num("11000000001000000000000000000000"), -2.5)

class TestNumOperations(unittest.TestCase):
    def test_binary_sum(self):
        self.assertEqual(binary_sum("1010", "1100"), "0000000000010110")
        self.assertEqual(binary_sum("1111", "0001"), "0000000000010000")
        self.assertEqual(binary_sum("0000", "0000"), "0000000000000000")

    def test_twos_complement_sum(self):
        self.assertEqual(twos_complement_sum(5, 3), ("0000000000001000", 8))
        self.assertEqual(twos_complement_sum(-5, -3), ("1111111111111000", -8))
        self.assertEqual(twos_complement_sum(5, -3), ("0000000000000010", 2))

    def test_twos_complement_diff(self):
        self.assertEqual(twos_complement_diff(5, 3), ("0000000000000010", 2))
        self.assertEqual(twos_complement_diff(-5, -3), ("1111111111111110", -2))
        self.assertEqual(twos_complement_diff(5, -3), ("0000000000001000", 8))

    def test_signed_multiply(self):
        self.assertEqual(signed_multiply(5, 3), ("0000000000001111", 15))
        self.assertEqual(signed_multiply(-5, 3), ("1000000000001111", -15))
        self.assertEqual(signed_multiply(5, -3), ("1000000000001111", -15))

    def test_signed_divide(self):
        self.assertEqual(signed_divide(10, 2), ("101.00000", 5.0))
        self.assertEqual(signed_divide(-10, 2), ("101.00000", -5.0))
        self.assertEqual(signed_divide(10, 3), ("11.01010", 3.3125))

    def test_float_add_ieee(self):
        self.assertEqual(float_add_ieee(1.5, 2.5), "01000000100000000000000000000000")
        self.assertEqual(float_add_ieee(-1.5, 2.5), "00111111100000000000000000000000")
        self.assertEqual(float_add_ieee(0, 0), IEEE754_NULL)

    def test_divide_by_zero(self):
        self.assertEqual(signed_divide(10, 0), ("Cannot divide by zero", None))

    def test_ieee754_invalid_input(self):
        self.assertEqual(ieee754_to_num("0000000000000000000000000000000"), 0.0)
        self.assertEqual(ieee754_to_num("invalid"), 0.0)

if __name__ == "__main__":
    unittest.main()