from settings import *

def num_to_binary(num):
    if num == 0:
        return "0"
    num = abs(num)
    bin_result = ""
    while num:
        bin_result = str(num % 2) + bin_result
        num //= 2
    return bin_result

def binary_to_decimal(bin_str):
    decimal = 0
    for i, bit in enumerate(reversed(bin_str)):
        if bit == "1":
            decimal += 1 << i
    return decimal

def num_to_signed_magnitude(num, bits=BIT_WIDTH):
    if num >= 0:
        bin_num = num_to_binary(num)
        return "0" * (bits - len(bin_num)) + bin_num
    bin_num = num_to_binary(-num)
    bin_num = "0" * (bits - 1 - len(bin_num)) + bin_num
    return "1" + bin_num

def num_to_ones_complement(num, bits=BIT_WIDTH):
    if num >= 0:
        bin_num = num_to_binary(num)
        return "0" * (bits - len(bin_num)) + bin_num
    bin_num = num_to_binary(-num)
    bin_num = "0" * (bits - 1 - len(bin_num)) + bin_num
    ones_comp = "".join("0" if bit == "1" else "1" for bit in bin_num)
    return "1" + ones_comp

def num_to_twos_complement(num, bits=BIT_WIDTH):
    if num >= 0:
        bin_num = num_to_binary(num)
        return "0" * (bits - len(bin_num)) + bin_num
    bin_num = num_to_binary(-num)
    bin_num = "0" * (bits - len(bin_num)) + bin_num
    ones_comp = "".join("0" if bit == "1" else "1" for bit in bin_num)
    result = ""
    carry = 1
    for bit in reversed(ones_comp):
        total = carry + int(bit)
        result = str(total % 2) + result
        carry = total // 2
    return result

def binary_to_decimal_twos(bin_str):
    if bin_str[0] == "0":
        return binary_to_decimal(bin_str)
    ones_comp = "".join("0" if bit == "1" else "1" for bit in bin_str)
    result = ""
    carry = 1
    for bit in reversed(ones_comp):
        total = carry + int(bit)
        result = str(total % 2) + result
        carry = total // 2
    return -binary_to_decimal(result)

def binary_to_decimal_signed(bin_str):
    return binary_to_decimal(bin_str[1:]) if bin_str[0] == "0" else -binary_to_decimal(bin_str[1:])

def num_to_ieee754(num):
    if num == 0:
        return IEEE754_NULL
    sign_bit = "0" if num > 0 else "1"
    num = abs(num)
    int_part = int(num)
    frac_part = num - int_part

    int_bin = num_to_binary(int_part) if int_part else "0"
    frac_bin = ""
    while frac_part:
        frac_part *= 2
        bit = 1 if frac_part >= 1 else 0
        frac_bin += str(bit)
        frac_part -= bit

    if int_bin != "0":
        exponent = len(int_bin) - 1
        mantissa = int_bin[1:] + frac_bin
    else:
        first_one = frac_bin.find("1")
        if first_one == -1:
            return IEEE754_NULL
        exponent = -(first_one + 1)
        mantissa = frac_bin[first_one + 1:]

    exponent += IEEE754_OFFSET
    exp_bin = ""
    for _ in range(IEEE754_EXP_LEN):
        exp_bin = str(exponent % 2) + exp_bin
        exponent //= 2

    mantissa = mantissa[:IEEE754_MANT_LEN] + "0" * (IEEE754_MANT_LEN - len(mantissa))
    return sign_bit + exp_bin + mantissa

def ieee754_to_num(ieee_str):
    if len(ieee_str) != IEEE754_TOTAL_BITS or ieee_str == IEEE754_NULL:
        return 0.0
    sign = -1 if ieee_str[0] == "1" else 1
    exp_bits = ieee_str[1:IEEE754_EXP_LEN + 1]
    mant_bits = ieee_str[IEEE754_EXP_LEN + 1:]

    exponent = sum(int(exp_bits[i]) * (1 << (IEEE754_EXP_LEN - 1 - i)) for i in range(IEEE754_EXP_LEN))
    exponent -= IEEE754_OFFSET

    mantissa = 1.0 + sum(int(mant_bits[i]) * (1.0 / (1 << (i + 1))) for i in range(IEEE754_MANT_LEN))
    return sign * mantissa * (2 ** exponent)