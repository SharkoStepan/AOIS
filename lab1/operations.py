from binary_converter import to_binary, to_complement, binary_to_decimal, fractional_to_binary, add_one, int_to_binary
from constants import BIT_SIZE, IEEE754_SIZE, EXPONENT_SIZE, MANTISSA_SIZE, EXPONENT_OFFSET, FRACTIONAL_PRECISION

def add_numbers(num1, num2):
    """Сложение двух чисел в дополнительном коде."""
    bin1 = to_complement(to_binary(num1, BIT_SIZE))
    bin2 = to_complement(to_binary(num2, BIT_SIZE))
    return add_numbers_binary(bin1, bin2)

def subtract_numbers(num1, num2):
    """Вычитание двух чисел в дополнительном коде."""
    bin1 = to_complement(to_binary(num1, BIT_SIZE))
    # Формируем дополнительный код для num2 (чтобы вычесть, добавляем -num2)
    bin2 = to_complement(to_binary(num2, BIT_SIZE))
    # Инвертируем bin2 и добавляем 1 для получения -num2
    bin2_inv = [1 - bit for bit in bin2]
    bin2_neg = add_one(bin2_inv)
    return binary_subtract(bin1, bin2_neg)

def multiply_numbers(num1, num2):
    """Умножение двух чисел с корректным учетом знака."""
    sign = 0 if (num1 >= 0) == (num2 >= 0) else 1
    abs_num1, abs_num2 = abs(num1), abs(num2)
    bin1 = to_binary(abs_num1, BIT_SIZE)[1:]  # Без знака
    bin2 = to_binary(abs_num2, BIT_SIZE)[1:]  # Без знака

    result = [0] * (2 * BIT_SIZE)

    for i in range(len(bin2) - 1, -1, -1):
        if bin2[i] == 1:
            temp = [0] * (2 * BIT_SIZE)
            shift = (len(bin2) - 1 - i)
            temp[-shift - len(bin1):-shift or None] = bin1

            carry = 0
            for j in range(len(result) - 1, -1, -1):
                sum_bits = result[j] + temp[j] + carry
                result[j] = sum_bits % 2
                carry = sum_bits // 2

    result = result[-BIT_SIZE:]

    if sign == 1:
        abs_result = binary_to_decimal([0] + result)
        neg_result = to_binary(-abs_result, BIT_SIZE)
        result = to_complement(neg_result)

    return result

def divide_numbers(num1, num2):
    """Деление двух чисел с корректным учетом знака и дробной части."""
    if num2 == 0:
        raise ValueError("Деление на ноль")
    
    sign = 0 if (num1 >= 0 and num2 >= 0) or (num1 < 0 and num2 < 0) else 1
    abs_num1, abs_num2 = abs(num1), abs(num2)
    
    int_part = abs_num1 // abs_num2
    remainder = abs_num1 % abs_num2
    
    int_code = to_binary(int_part, BIT_SIZE)
    if sign == 1:
        int_code = to_complement([1] + int_code[1:])
    
    frac_part = []
    for _ in range(FRACTIONAL_PRECISION):
        remainder *= 2
        bit = 1 if remainder >= abs_num2 else 0
        frac_part.append(bit)
        if bit:
            remainder -= abs_num2
        if remainder == 0:
            frac_part += [0] * (FRACTIONAL_PRECISION - len(frac_part))
            break
    
    return int_code, frac_part

def shift_left(number, bit):
    """Сдвиг влево с добавлением нового бита."""
    result = number[1:] + [bit]
    return result

def binary_compare(a, b):
    """Сравнение двух двоичных чисел."""
    def binary_to_int(bits):
        if bits[0] == 1:  # Отрицательное число
            inverted = [1 - bit for bit in bits[1:]]
            complement = add_one([0] + inverted)
            return -sum(2 ** (len(complement) - 1 - i) * bit for i, bit in enumerate(complement))
        return sum(2 ** (len(bits) - 1 - i) * bit for i, bit in enumerate(bits[1:]))

    a_val = binary_to_int(a)
    b_val = binary_to_int(b)
    return 0 if a_val == b_val else 1 if a_val > b_val else -1

def binary_subtract(a, b):
    """Вычитание двоичных чисел через сложение с дополнительным кодом."""
    a = [0] * (BIT_SIZE - len(a)) + a[-BIT_SIZE:]
    b = [0] * (BIT_SIZE - len(b)) + b[-BIT_SIZE:]

    # Инвертируем b и добавляем 1 для получения -b
    b_inv = [1 - bit for bit in b]
    b_neg = add_one(b_inv)

    # Выполняем сложение a + (-b)
    max_len = BIT_SIZE
    result = [0] * max_len
    carry = 0
    for i in range(max_len - 1, -1, -1):
        total = a[i] + b_neg[i] + carry
        result[i] = total % 2
        carry = total // 2

    return result[-BIT_SIZE:]

def add_numbers_binary(bin1, bin2):
    """Сложение двух чисел в двоичном формате."""
    max_len = max(len(bin1), len(bin2))
    bin1 = [0] * (max_len - len(bin1)) + bin1
    bin2 = [0] * (max_len - len(bin2)) + bin2

    result = [0] * max_len
    carry = 0

    for i in range(max_len - 1, -1, -1):
        total = bin1[i] + bin2[i] + carry
        result[i] = total % 2
        carry = total // 2

    return result[-BIT_SIZE:]

def float_to_ieee754(num):
    """Преобразование числа с плавающей точкой в IEEE-754."""
    if num == 0:
        return [0] * IEEE754_SIZE
    sign = 0 if num >= 0 else 1
    num = abs(num)
    int_part = int(num)
    frac_part = num - int_part
    int_bin = int_to_binary(int_part) or [0]
    frac_bin = fractional_to_binary(frac_part, MANTISSA_SIZE + 1)
    binary = int_bin + frac_bin
    if int_bin != [0]:
        exp = len(int_bin) - 1
        mantissa = binary[1:1 + MANTISSA_SIZE]
    else:
        first_one = next((i for i, bit in enumerate(frac_bin) if bit == 1), len(frac_bin))
        if first_one == len(frac_bin):
            return [sign] + [0] * (EXPONENT_SIZE + MANTISSA_SIZE)
        exp = - (first_one + 1)
        mantissa = frac_bin[first_one + 1:first_one + 1 + MANTISSA_SIZE]
    mantissa += [0] * (MANTISSA_SIZE - len(mantissa))
    biased_exp = exp + EXPONENT_OFFSET

    def unsigned_binary(num, bits):
        result = []
        while num > 0:
            result.insert(0, num % 2)
            num //= 2
        return [0] * (bits - len(result)) + result

    exp_binary = unsigned_binary(biased_exp, EXPONENT_SIZE)
    return [sign] + exp_binary + mantissa

def add_ieee754(num1, num2):
    """Сложение двух чисел в формате IEEE-754."""
    bin1 = float_to_ieee754(num1)
    bin2 = float_to_ieee754(num2)
    
    sign1, sign2 = bin1[0], bin2[0]
    exp1 = sum(2 ** (EXPONENT_SIZE - 1 - i) * bit for i, bit in enumerate(bin1[1:1 + EXPONENT_SIZE]))
    exp2 = sum(2 ** (EXPONENT_SIZE - 1 - i) * bit for i, bit in enumerate(bin2[1:1 + EXPONENT_SIZE]))
    mant1 = [1] + bin1[1 + EXPONENT_SIZE:] if exp1 != 0 else [0] + bin1[1 + EXPONENT_SIZE:]
    mant2 = [1] + bin2[1 + EXPONENT_SIZE:] if exp2 != 0 else [0] + bin2[1 + EXPONENT_SIZE:]

    if exp1 > exp2:
        shift = exp1 - exp2
        mant2 = [0] * shift + mant2[:-shift] if shift > 0 else mant2
        exponent = exp1
    else:
        shift = exp2 - exp1
        mant1 = [0] * shift + mant1[:-shift] if shift > 0 else mant1
        exponent = exp2

    mant1_val = sum(2 ** (len(mant1) - 1 - i) * bit for i, bit in enumerate(mant1)) * (-1 if sign1 else 1)
    mant2_val = sum(2 ** (len(mant2) - 1 - i) * bit for i, bit in enumerate(mant2)) * (-1 if sign2 else 1)
    mant_result = mant1_val + mant2_val

    if mant_result == 0:
        return [0] * IEEE754_SIZE
    sign_result = 0 if mant_result >= 0 else 1
    mant_result = abs(mant_result)
    shift = 0
    while mant_result >= (1 << (MANTISSA_SIZE + 1)):
        mant_result >>= 1
        exponent += 1
        shift += 1
    while mant_result < (1 << MANTISSA_SIZE) and mant_result != 0:
        mant_result <<= 1
        exponent -= 1
        shift -= 1

    # Возвращаем бесконечность вместо исключения
    if exponent >= 255:
        return [sign_result] + [1] * EXPONENT_SIZE + [0] * MANTISSA_SIZE
    if exponent <= 0:
        # Денормализованное число
        mantissa_shift = 1 - exponent
        mant_result >>= mantissa_shift
        exponent = 0

    mant_bits = []
    temp = mant_result
    for _ in range(MANTISSA_SIZE + 1):
        mant_bits.insert(0, temp % 2)
        temp //= 2
    mant_bits = mant_bits[1:MANTISSA_SIZE + 1]
    exp_bits = []
    temp = exponent
    for _ in range(EXPONENT_SIZE):
        exp_bits.insert(0, temp % 2)
        temp //= 2
    return [sign_result] + exp_bits + mant_bits

def ieee754_to_float(binary):
    """Преобразование IEEE-754 в число с плавающей точкой."""
    if all(bit == 0 for bit in binary):
        return 0.0
    sign = -1 if binary[0] == 1 else 1
    exp = sum(2 ** (EXPONENT_SIZE - 1 - i) * bit for i, bit in enumerate(binary[1:1 + EXPONENT_SIZE])) - EXPONENT_OFFSET
    mantissa = 1.0 + sum(bit * (2 ** -(i + 1)) for i, bit in enumerate(binary[1 + EXPONENT_SIZE:]))
    return sign * mantissa * (2 ** exp)