from numerical_representations import *
from arithmetic_processor import *


def main_controller():
    print("Система числовой обработки активирована!")
    while True:
        print("\nДоступные операции:")
        print("1. Целочисленные вычисления")
        print("2. Операции с плавающей точкой")
        print("3. Выход")
        choice = input("Выберите операцию: ")

        if choice == "1":
            process_integer_operations()
        elif choice == "2":
            process_float_operations()
        elif choice == "3":
            print("Завершение работы.")
            break
        else:
            print("Неверный выбор!")


def process_integer_operations():
    try:
        num1 = int(input("Первое целое число: "))
        num2 = int(input("Второе целое число: "))
    except ValueError:
        print("Ошибка ввода!")
        return

    display_conversions(num1, num2)
    display_arithmetic_results(num1, num2)


def process_float_operations():
    try:
        f1 = float(input("Первое число с плавающей точкой: "))
        f2 = float(input("Второе число с плавающей точкой: "))
    except ValueError:
        print("Ошибка ввода!")
        return

    result_bits, result_value = floating_point_addition_with_bits(f1, f2)
    print(f"\nСложение в формате IEEE-754:")
    print(f"{f1} + {f2} = {result_value}")
    print(f"Двоичное представление: {result_bits}")


def display_conversions(a, b):
    print("\n--- Представления чисел ---")
    for num in [a, b]:
        print(f"Число {num}:")
        print(f"  Двоичное: {integer_to_binary_string(num)}")
        print(f"  Прямой код: {direct_code_representation(num)}")
        print(f"  Обратный код: {ones_complement_representation(num)}")
        print(f"  Дополнительный код: {complement_representation(num)}")


def display_arithmetic_results(a, b):
    print("\n--- Арифметические операции ---")

    # Сложение
    sum_bits, sum_value = addition_with_binary(a, b)
    print(f"Сложение: {a} + {b} = {sum_value}")
    print(f"  Двоичный результат: {sum_bits}")

    # Вычитание
    diff_bits, diff_value = subtraction_with_binary(a, b)
    print(f"Вычитание: {a} - {b} = {diff_value}")
    print(f"  Двоичный результат: {diff_bits}")

    # Умножение
    mul_bits, mul_value = multiplication_with_binary(a, b)
    print(f"Умножение: {a} × {b} = {mul_value}")
    print(f"  Двоичный результат: {mul_bits}")

    # Деление
    if b != 0:
        div_bits, div_value = division_with_binary(a, b)
        print(f"Деление: {a} ÷ {b} = {div_value}")
        print(f"  Двоичный результат: {div_bits}")
    else:
        print("Деление на ноль невозможно!")


if __name__ == "__main__":
    main_controller()
