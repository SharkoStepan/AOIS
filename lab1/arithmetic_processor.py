from numerical_representations import *


def binary_addition(bin1, bin2):
    """Сложение двух двоичных строк"""
    if bin1 == "0" and bin2 == "0":
        return "0"

    # Убираем ведущие нули
    bin1 = bin1.lstrip('0') or '0'
    bin2 = bin2.lstrip('0') or '0'

    result = []
    carry = 0
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    for i in range(max_len - 1, -1, -1):
        bit1 = int(bin1[i])
        bit2 = int(bin2[i])

        total = bit1 + bit2 + carry
        result.append(str(total % 2))
        carry = total // 2

    if carry:
        result.append('1')

    result_str = ''.join(reversed(result))
    return result_str.lstrip('0') or '0'


def addition_with_binary(a, b):
    """Сложение с возвратом двоичного результата"""
    result_decimal = a + b

    # Получаем двоичное представление результата
    result_binary = integer_to_binary_string(result_decimal)

    # Для совместимости с тестами возвращаем обрезанную версию без ведущих нулей
    clean_binary = result_binary.lstrip('0') or '0'
    return clean_binary, result_decimal


def subtraction_with_binary(a, b):
    """Вычитание с возвратом двоичного результата"""
    result_decimal = a - b
    result_binary = integer_to_binary_string(result_decimal)
    clean_binary = result_binary.lstrip('0') or '0'
    return clean_binary, result_decimal


def multiplication_with_binary(a, b):
    """Умножение с возвратом двоичного результата"""
    result_decimal = a * b
    result_binary = integer_to_binary_string(result_decimal)
    clean_binary = result_binary.lstrip('0') or '0'
    return clean_binary, result_decimal


def division_with_binary(a, b):
    """Деление с возвратом двоичного результата"""
    if b == 0:
        return "ERROR", "Деление на ноль"

    # Целая часть
    integer_part = a // b
    remainder = a % b

    # Дробная часть (5 битов)
    fractional = 0
    precision = 5
    for i in range(precision):
        remainder *= 2
        if remainder >= b:
            fractional += 1 << (precision - i - 1)
            remainder -= b

    # Комбинируем результат
    result_decimal = integer_part + fractional / (1 << precision)

    # Для простоты представляем только целую часть в двоичном виде
    result_binary = integer_to_binary_string(integer_part) + "." + bin(fractional)[2:].zfill(precision)

    return result_binary, result_decimal


def floating_point_addition_with_bits(a, b):
    """Сложение чисел с плавающей точкой с возвратом битов"""
    result_value = a + b  # Используем встроенное сложение для простоты
    result_bits = ieee754_representation(result_value)
    return result_bits, result_value


def bitwise_operations(a, b):
    """Побитовые операции для демонстрации"""
    and_result = a & b
    or_result = a | b
    xor_result = a ^ b

    print(f"Побитовые операции:")
    print(
        f"  AND: {integer_to_binary_string(a)} & {integer_to_binary_string(b)} = {integer_to_binary_string(and_result)}")
    print(
        f"  OR:  {integer_to_binary_string(a)} | {integer_to_binary_string(b)} = {integer_to_binary_string(or_result)}")
    print(
        f"  XOR: {integer_to_binary_string(a)} ^ {integer_to_binary_string(b)} = {integer_to_binary_string(xor_result)}")


def run_comprehensive_test():
    """Комплексный тест всех операций"""
    print("Комплексное тестирование системы:")

    test_cases = [
        (15, 7),
        (-8, 3),
        (100, 25),
        (0, 5)
    ]

    for a, b in test_cases:
        print(f"\nТест для чисел {a} и {b}:")

        # Сложение
        bin_res, dec_res = addition_with_binary(a, b)
        print(f"  Сложение: {a} + {b} = {dec_res} (бинарно: {bin_res})")

        # Вычитание
        bin_res, dec_res = subtraction_with_binary(a, b)
        print(f"  Вычитание: {a} - {b} = {dec_res} (бинарно: {bin_res})")

        # Умножение
        bin_res, dec_res = multiplication_with_binary(a, b)
        print(f"  Умножение: {a} × {b} = {dec_res} (бинарно: {bin_res})")

        if b != 0:
            bin_res, dec_res = division_with_binary(a, b)
            print(f"  Деление: {a} ÷ {b} = {dec_res} (бинарно: {bin_res})")


# Дополнительные утилиты
def demonstrate_float_operations():
    """Демонстрация операций с плавающей точкой"""
    test_values = [
        (1.5, 2.5),
        (3.14, 1.59),
        (-2.75, 1.25)
    ]

    print("\nДемонстрация IEEE-754 операций:")
    for a, b in test_values:
        bits_a = ieee754_representation(a)
        bits_b = ieee754_representation(b)
        result_bits, result_value = floating_point_addition_with_bits(a, b)

        print(f"\n{a} + {b} = {result_value}")
        print(f"  IEEE-754 {a}: {bits_a}")
        print(f"  IEEE-754 {b}: {bits_b}")
        print(f"  Результат: {result_bits}")


if __name__ == "__main__":
    run_comprehensive_test()
    demonstrate_float_operations()