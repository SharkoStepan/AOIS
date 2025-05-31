from operations import add_numbers, subtract_numbers, multiply_numbers, divide_numbers, float_to_ieee754, add_ieee754, ieee754_to_float
from binary_converter import to_binary, to_complement, binary_to_decimal
from constants import BIT_SIZE

def display_codes(num, label):
    """Выводит коды числа."""
    direct = to_binary(num, BIT_SIZE)
    inverse = [1 - bit if i > 0 and direct[0] == 1 else bit for i, bit in enumerate(direct)]
    complement = to_complement(direct)
    print(f"{label}: {num}")
    print(f"Прямой код: {direct}")
    print(f"Обратный код: {inverse}")
    print(f"Дополнительный код: {complement}")

def main():
    """Основная функция программы."""
    # Сложение
    print("Сложение в дополнительном коде:")
    num1 = int(input("Ввод числа №1: "))
    display_codes(num1, "Число введено")
    num2 = int(input("Ввод числа №2: "))
    display_codes(num2, "Число введено")
    result = add_numbers(num1, num2)
    decimal_result = binary_to_decimal(result)
    print(f"Результат: {decimal_result}")
    display_codes(decimal_result, "Число введено")

    # Вычитание
    print("\nВычитание в дополнительном коде:")
    num1 = int(input("Ввод числа №1: "))
    display_codes(num1, "Число введено")
    num2 = int(input("Ввод числа №2: "))
    display_codes(num2, "Число введено")
    result = subtract_numbers(num1, num2)
    decimal_result = binary_to_decimal(result)
    print(f"Результат: {decimal_result}")
    display_codes(decimal_result, "Число введено")

    # Умножение
    print("\nУмножение в прямом коде:")
    num1 = int(input("Ввод числа №1: "))
    display_codes(num1, "Число введено")
    num2 = int(input("Ввод числа №2: "))
    display_codes(num2, "Число введено")
    result = multiply_numbers(num1, num2)
    decimal_result = binary_to_decimal(result)
    print(f"multiply result (binary): {result}")
    print(f"Результат: {decimal_result}")
    display_codes(decimal_result, "Число введено")

    # Деление
    print("\nДеление в прямом коде:")
    num1 = int(input("Ввод числа №1: "))
    display_codes(num1, "Число введено")
    num2 = int(input("Ввод числа №2: "))
    display_codes(num2, "Число введено")
    try:
        int_part, frac_part = divide_numbers(num1, num2)
        int_value = binary_to_decimal(int_part)
        frac_value = sum(b * (2 ** -(i + 1)) for i, b in enumerate(frac_part))
        decimal_result = int_value + frac_value if int_value >= 0 else int_value - frac_value
        print(f"int_part (binary): {int_part}, int_value: {int_value}, frac_value: {frac_value}")
        print(f"Результат: {decimal_result:.5f}")
        print(f"Целая часть (прямой код): {int_part}")
        print(f"Дробная часть (двоичный): {frac_part}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # IEEE-754
    print("\nСложение чисел с плавающей точкой (IEEE-754):")
    num1 = float(input("Ввод числа №1: "))
    bin1 = float_to_ieee754(num1)
    print(f"Число {num1} в IEEE-754: {bin1}")
    num2 = float(input("Ввод числа №2: "))
    bin2 = float_to_ieee754(num2)
    print(f"Число {num2} в IEEE-754: {bin2}")
    result = add_ieee754(num1, num2)
    decimal_result = ieee754_to_float(result)
    print(f"Результат: {decimal_result:.5f}")
    print(f"Результат в IEEE-754: {result}")

if __name__ == "__main__":
    main()