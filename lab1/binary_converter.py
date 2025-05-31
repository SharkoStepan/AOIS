from constants import BIT_SIZE

def to_binary(number, length):
    """Преобразование числа в прямой двоичный код."""
    if number >= 0:
        sign = 0
        binary = []
        while number > 0:
            binary.insert(0, number % 2)
            number //= 2
        binary = [sign] + [0] * (length - len(binary) - 1) + binary
    else:
        sign = 1
        number = abs(number)
        binary = []
        while number > 0:
            binary.insert(0, number % 2)
            number //= 2
        binary = [sign] + [0] * (length - len(binary) - 1) + binary
    return binary[-length:]

def to_complement(binary):
    """Преобразование прямого кода в дополнительный."""
    if binary[0] == 0:
        return binary
    inverted = [1 - bit for bit in binary[1:]]
    return [1] + add_one(inverted)

def binary_to_decimal(binary):
    """Преобразование дополнительного кода в десятичное число."""
    if binary[0] == 0:
        return sum(2 ** (len(binary) - 2 - i) * bit for i, bit in enumerate(binary[1:]))
    inverted = [1 - bit for bit in binary[1:]]
    complement = add_one([0] + inverted)[1:]
    return -sum(2 ** (len(complement) - 1 - i) * bit for i, bit in enumerate(complement))

def add_one(binary):
    """Добавление единицы к двоичному числу."""
    result = binary.copy()
    carry = 1
    for i in range(len(result) - 1, -1, -1):
        total = result[i] + carry
        result[i] = total % 2
        carry = total // 2
    return result

def int_to_binary(number):
    """Преобразование целого числа в двоичный список (без знака)."""
    if number == 0:
        return [0]
    binary = []
    while number > 0:
        binary.insert(0, number % 2)
        number //= 2
    return binary

def fractional_to_binary(number, precision):
    """Преобразование дробной части в двоичный список."""
    binary = []
    while number > 0 and len(binary) < precision:
        number *= 2
        bit = int(number)
        binary.append(bit)
        number -= bit
    return binary + [0] * (precision - len(binary))