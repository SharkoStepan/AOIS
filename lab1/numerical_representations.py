class BinaryConverter:
    def __init__(self, bit_width=16):
        self.bit_width = bit_width
        self.max_value = (1 << bit_width) - 1
        self.min_value = -(1 << (bit_width - 1))

    def to_binary(self, number):
        """Преобразование целого числа в двоичную строку"""
        if number >= 0:
            binary = bin(number)[2:].zfill(self.bit_width)
            return binary[-self.bit_width:]  # Обрезаем до нужной длины
        else:
            # Для отрицательных используем дополнительный код
            positive = (1 << self.bit_width) + number
            return bin(positive)[2:].zfill(self.bit_width)

    def from_binary(self, binary_str):
        """Преобразование двоичной строки в целое число"""
        if len(binary_str) != self.bit_width:
            binary_str = binary_str.zfill(self.bit_width)

        if binary_str[0] == '1':  # Отрицательное число в дополнительном коде
            value = int(binary_str, 2)
            if value >= (1 << (self.bit_width - 1)):
                value -= (1 << self.bit_width)
            return value
        else:
            return int(binary_str, 2)

    def ones_complement(self, number):
        """Обратный код"""
        if number >= 0:
            return self.to_binary(number)
        else:
            positive_binary = self.to_binary(-number)
            inverted = ''.join('1' if bit == '0' else '0' for bit in positive_binary)
            return inverted

    def signed_magnitude(self, number):
        """Прямой код"""
        sign_bit = '0' if number >= 0 else '1'
        magnitude = bin(abs(number))[2:].zfill(self.bit_width - 1)
        return sign_bit + magnitude


class IEEE754Converter:
    def __init__(self):
        self.exponent_bits = 8
        self.mantissa_bits = 23
        self.bias = 127
        self.total_bits = 32

    def float_to_bits(self, number):
        """Преобразование float в IEEE754 через математические операции"""
        if number == 0.0:
            return '0' * self.total_bits

        # Определяем знак
        sign_bit = '0' if number >= 0 else '1'
        number = abs(number)

        # Нормализуем число
        exponent = 0
        if number >= 2.0:
            while number >= 2.0:
                number /= 2.0
                exponent += 1
        elif number < 1.0:
            while number < 1.0:
                number *= 2.0
                exponent -= 1

        # Вычисляем мантиссу
        number -= 1.0  # Убираем неявную единицу
        mantissa = ''
        for _ in range(self.mantissa_bits):
            number *= 2.0
            if number >= 1.0:
                mantissa += '1'
                number -= 1.0
            else:
                mantissa += '0'

        # Вычисляем экспоненту
        exponent += self.bias
        exponent_bits = bin(exponent)[2:].zfill(self.exponent_bits)

        return sign_bit + exponent_bits + mantissa

    def bits_to_float(self, bits):
        """Преобразование битов IEEE754 в float"""
        if bits == '0' * self.total_bits:
            return 0.0

        sign_bit = bits[0]
        exponent_bits = bits[1:1 + self.exponent_bits]
        mantissa_bits = bits[1 + self.exponent_bits:]

        # Экспонента
        exponent = int(exponent_bits, 2) - self.bias

        # Мантисса
        mantissa = 1.0  # Неявная единица
        for i, bit in enumerate(mantissa_bits):
            if bit == '1':
                mantissa += 2.0 ** (-i - 1)

        # Финальное значение
        result = mantissa * (2.0 ** exponent)
        return -result if sign_bit == '1' else result


# Глобальные экземпляры конвертеров
binary_converter = BinaryConverter()
ieee_converter = IEEE754Converter()


def integer_to_binary_string(number):
    return binary_converter.to_binary(number)


def binary_string_to_integer(binary_str):
    return binary_converter.from_binary(binary_str)


def direct_code_representation(number):
    return binary_converter.signed_magnitude(number)


def ones_complement_representation(number):
    return binary_converter.ones_complement(number)


def complement_representation(number):
    return binary_converter.to_binary(number)


def ieee754_representation(number):
    return ieee_converter.float_to_bits(number)


def ieee754_to_float(bits):
    return ieee_converter.bits_to_float(bits)
