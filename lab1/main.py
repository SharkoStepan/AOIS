from num_operations import *

def main():
    print("Программа для операций с числами запущена!")
    while True:
        print("\nМеню операций:")
        print("1. Работа с целыми числами (конвертация, сложение, вычитание, умножение, деление)")
        print("2. Сложение чисел с плавающей точкой (IEEE-754)")
        print("3. Завершить программу")
        user_choice = input("Выберите опцию: ")

        if user_choice == "1":
            try:
                number1 = int(input("Введите первое целое число: "))
                number2 = int(input("Введите второе целое число: "))
            except ValueError:
                print("Ошибка: введите корректные целые числа.")
                continue

            print("\nРезультаты конвертации в двоичный формат:")
            print(f"Прямой код для {number1}: {num_to_signed_magnitude(number1)}")
            print(f"Обратный код для {number1}: {num_to_ones_complement(number1)}")
            print(f"Дополнительный код для {number1}: {num_to_twos_complement(number1)}")
            print(f"Прямой код для {number2}: {num_to_signed_magnitude(number2)}")
            print(f"Обратный код для {number2}: {num_to_ones_complement(number2)}")
            print(f"Дополнительный код для {number2}: {num_to_twos_complement(number2)}")

            result_bin_sum, result_dec_sum = twos_complement_sum(number1, number2)
            print(f"\nСложение ({number1} + {number2}):")
            print(f"Результат в двоичном виде: {result_bin_sum}")
            print(f"Результат в десятичном виде: {result_dec_sum}")

            result_bin_diff, result_dec_diff = twos_complement_diff(number1, number2)
            print(f"\nВычитание ({number1} - {number2}):")
            print(f"Результат в двоичном виде: {result_bin_diff}")
            print(f"Результат в десятичном виде: {result_dec_diff}")

            result_bin_mul, result_dec_mul = signed_multiply(number1, number2)
            print(f"\nУмножение ({number1} * {number2}):")
            print(f"Результат в двоичном виде: {result_bin_mul}")
            print(f"Результат в десятичном виде: {result_dec_mul}")

            if number2 == 0:
                print("\nОшибка: деление на ноль невозможно!")
            else:
                result_bin_div, result_dec_div = signed_divide(number1, number2)
                print(f"\nДеление ({number1} / {number2}):")
                print(f"Результат в двоичном виде: {result_bin_div}")
                print(f"Результат в десятичном виде: {result_dec_div}")

        elif user_choice == "2":
            try:
                float_num1 = float(input("Введите первое число с плавающей точкой: "))
                float_num2 = float(input("Введите второе число с плавающей точкой: "))
            except ValueError:
                print("Ошибка: введите корректные числа с плавающей точкой.")
                continue

            ieee_sum = float_add_ieee(float_num1, float_num2)
            decimal_sum = ieee754_to_num(ieee_sum)
            print(f"\nСложение в формате IEEE-754 ({float_num1} + {float_num2}):")
            print(f"Результат в двоичном виде: {ieee_sum}")
            print(f"Результат в десятичном виде: {decimal_sum}")

        elif user_choice == "3":
            print("Программа завершена.")
            break

        else:
            print("Ошибка: выберите опцию 1, 2 или 3.")

if __name__ == "__main__":
    main()