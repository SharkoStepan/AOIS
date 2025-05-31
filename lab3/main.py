from logic_parser import generate_truth_table, print_truth_table
from minimizer import (
    minimize_sdnf_calc_method, minimize_sknf_calc_method,
    minimize_sdnf_table_method, minimize_sknf_table_method,
    minimize_sdnf_kmap_method, minimize_sknf_kmap_method
)

def main():
    try:
        expr = input("Введите логическую функцию (операторы: ! & | ->, переменные: a,b,c,d,e):\n")
        variables, table = generate_truth_table(expr)

        print("\nТаблица истинности:")
        print_truth_table(variables, table)

        print("\nМинимизация СДНФ (расчетный метод):")
        result_sdnf_calc = minimize_sdnf_calc_method(variables, table)
        print(f"Результат: {result_sdnf_calc}")

        print("\nМинимизация СКНФ (расчетный метод):")
        result_sknf_calc = minimize_sknf_calc_method(variables, table)
        print(f"Результат: {result_sknf_calc}")

        print("\nМинимизация СДНФ (табличный метод):")
        result_sdnf_table = minimize_sdnf_table_method(variables, table)
        print(f"Результат: {result_sdnf_table}")

        print("\nМинимизация СКНФ (табличный метод):")
        result_sknf_table = minimize_sknf_table_method(variables, table)
        print(f"Результат: {result_sknf_table}")

        print("\nМинимизация СДНФ (метод карты Карно):")
        result_sdnf_kmap = minimize_sdnf_kmap_method(variables, table)
        print(f"Результат: {result_sdnf_kmap}")

        print("\nМинимизация СКНФ (метод карты Карно):")
        result_sknf_kmap = minimize_sknf_kmap_method(variables, table)
        print(f"Результат: {result_sknf_kmap}")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()