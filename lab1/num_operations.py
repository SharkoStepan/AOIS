from num_converters import *
from settings import *

def binary_sum(bin_str1, bin_str2, bit_len=BIT_WIDTH):
    carry_bit = 0
    result_str = ""
    bin_str1 = "0" * (bit_len - len(bin_str1)) + bin_str1
    bin_str2 = "0" * (bit_len - len(bin_str2)) + bin_str2

    for idx in range(bit_len - 1, -1, -1):
        temp = carry_bit
        temp += int(bin_str1[idx])
        temp += int(bin_str2[idx])
        result_str = str(temp % 2) + result_str
        carry_bit = temp // 2
    return result_str

def twos_complement_sum(num_a, num_b, bit_len=BIT_WIDTH):
    bin_a = num_to_binary(num_a) if num_a >= 0 else num_to_twos_complement(num_a, bit_len)
    bin_a = "0" * (bit_len - len(bin_a)) + bin_a
    bin_b = num_to_binary(num_b) if num_b >= 0 else num_to_twos_complement(num_b, bit_len)
    bin_b = "0" * (bit_len - len(bin_b)) + bin_b
    sum_bin = binary_sum(bin_a, bin_b, bit_len)
    sum_dec = binary_to_decimal_twos(sum_bin)
    return sum_bin, sum_dec

def twos_complement_diff(num_a, num_b, bit_len=BIT_WIDTH):
    bin_a = num_to_twos_complement(num_a, bit_len)
    bin_b = num_to_twos_complement(-num_b, bit_len)
    diff_bin = binary_sum(bin_a, bin_b, bit_len)
    diff_dec = binary_to_decimal_twos(diff_bin)
    return diff_bin, diff_dec

def signed_multiply(val1, val2, bit_len=BIT_WIDTH):
    sign_result = 1 if (val1 >= 0) == (val2 >= 0) else -1
    abs_val1 = abs(val1)
    abs_val2 = abs(val2)

    bin_val1 = num_to_binary(abs_val1)
    bin_val1 = "0" * (bit_len - len(bin_val1)) + bin_val1
    bin_val2 = num_to_binary(abs_val2)
    bin_val2 = "0" * (bit_len - len(bin_val2)) + bin_val2

    product = 0
    for pos in range(bit_len - 1, -1, -1):
        if bin_val2[pos] == "1":
            shift = binary_to_decimal(bin_val1) << (bit_len - 1 - pos)
            product += shift

    bin_product = num_to_binary(product)
    if len(bin_product) > bit_len:
        bin_product = bin_product[-bit_len:]
    else:
        bin_product = "0" * (bit_len - len(bin_product)) + bin_product

    bin_product = ("1" if sign_result == -1 else "0") + bin_product[1:]
    dec_product = product if sign_result == 1 else -product
    return bin_product, dec_product

def signed_divide(num1, num2, bit_len=BIT_WIDTH, precision=FRAC_PREC):
    if num2 == 0:
        return "Cannot divide by zero", None

    sign = 1 if (num1 >= 0) == (num2 >= 0) else -1
    abs_num1 = abs(num1)
    abs_num2 = abs(num2)

    quotient = 0
    while abs_num1 >= abs_num2:
        abs_num1 -= abs_num2
        quotient += 1

    bin_whole = num_to_binary(quotient)
    bin_frac = ""
    remainder = abs_num1
    for _ in range(precision):
        remainder *= 2
        bit = 1 if remainder >= abs_num2 else 0
        bin_frac += str(bit)
        if bit:
            remainder -= abs_num2

    result_bin = bin_whole + "." + bin_frac
    result_dec = quotient
    frac_value = 0
    power = -1
    for bit in bin_frac:
        if bit == "1":
            frac_value += 2 ** power
        power -= 1
    result_dec += frac_value
    if sign == -1:
        result_dec = -result_dec

    return result_bin, result_dec

def float_add_ieee(num1, num2):
    if num1 == 0 and num2 == 0:
        return IEEE754_NULL

    bin_num1 = num_to_ieee754(num1)
    bin_num2 = num_to_ieee754(num2)

    sign1 = -1 if bin_num1[0] == "1" else 1
    exp1 = sum(int(bin_num1[i + 1]) * (1 << (IEEE754_EXP_LEN - 1 - i)) for i in range(IEEE754_EXP_LEN))
    exp1 -= IEEE754_OFFSET

    mant1 = 1.0
    for i in range(IEEE754_MANT_LEN):
        mant1 += int(bin_num1[9 + i]) * (1.0 / (1 << (i + 1)))

    sign2 = -1 if bin_num2[0] == "1" else 1
    exp2 = sum(int(bin_num2[i + 1]) * (1 << (IEEE754_EXP_LEN - 1 - i)) for i in range(IEEE754_EXP_LEN))
    exp2 -= IEEE754_OFFSET

    mant2 = 1.0
    for i in range(IEEE754_MANT_LEN):
        mant2 += int(bin_num2[9 + i]) * (1.0 / (1 << (i + 1)))

    if exp1 > exp2:
        mant2 /= (1 << (exp1 - exp2))
        exp2 = exp1
    else:
        mant1 /= (1 << (exp2 - exp1))
        exp1 = exp2

    result_mant = sign1 * mant1 + sign2 * mant2
    result_sign = "1" if result_mant < 0 else "0"
    result_mant = abs(result_mant)

    if result_mant == 0:
        return IEEE754_NULL

    while result_mant >= 2.0:
        result_mant /= 2.0
        exp1 += 1
    while result_mant < 1.0:
        result_mant *= 2.0
        exp1 -= 1

    exp_bin = ""
    exp1 += IEEE754_OFFSET
    for _ in range(IEEE754_EXP_LEN):
        exp_bin = str(exp1 % 2) + exp_bin
        exp1 //= 2

    mant_bin = ""
    result_mant -= 1.0
    for _ in range(IEEE754_MANT_LEN):
        result_mant *= 2
        bit = 1 if result_mant >= 1 else 0
        mant_bin += str(bit)
        result_mant -= bit

    return result_sign + exp_bin + mant_bin