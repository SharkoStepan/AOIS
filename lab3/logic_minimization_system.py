from expression_processor import LogicalExpressionProcessor
from minimization_engine import MinimizationEngine
from truth_table_generator import TruthTableGenerator
from results_presenter import ResultsPresenter


class LogicMinimizationSystem:
    def __init__(self):
        self.expression_processor = LogicalExpressionProcessor()
        self.minimization_engine = MinimizationEngine()
        self.truth_table_generator = TruthTableGenerator()
        self.results_presenter = ResultsPresenter()

    def execute_minimization_pipeline(self, input_expression):
        """Основной пайплайн обработки логического выражения"""
        try:
            # Валидация и парсинг выражения
            validated_data = self.expression_processor.validate_and_parse(input_expression)
            if not validated_data["is_valid"]:
                return {"error": validated_data["error_message"]}

            # Генерация таблицы истинности
            truth_table_data = self.truth_table_generator.generate_complete_table(
                validated_data["variables"],
                validated_data["postfix_tokens"]
            )

            # Получаем отформатированную таблицу истинности
            table_display = self.truth_table_generator.get_truth_table_display(truth_table_data)

            # Получаем информацию о минтермах и макстермах
            minterm_info = self.truth_table_generator.get_minterm_maxterm_info(truth_table_data)

            # Минимизация различными методами
            minimization_results = self.minimization_engine.perform_all_minimizations(
                truth_table_data,
                validated_data["variables"]
            )

            # Добавляем дополнительную информацию в результаты
            minimization_results["truth_table_display"] = table_display
            minimization_results["minterm_info"] = minterm_info

            # Презентация результатов
            return self.results_presenter.format_comprehensive_results(minimization_results)

        except Exception as e:
            return {"error": f"Системная ошибка: {str(e)}"}


def main():
    system = LogicMinimizationSystem()

    print("=== СИСТЕМА МИНИМИЗАЦИИ ЛОГИЧЕСКИХ ФУНКЦИЙ ===")
    print("Поддерживаемые операторы: & (И), | (ИЛИ), ! (НЕ), -> (импликация), ~ (эквивалентность)")
    print("Доступные переменные: a, b, c, d, e")
    print("Пример: (a & b) | (!c -> d)")

    while True:
        print("\n" + "=" * 50)
        user_input = input("Введите логическое выражение (или 'exit' для выхода): ").strip()

        if user_input.lower() == 'exit':
            print("Завершение работы системы.")
            break

        if not user_input:
            print("Ошибка: пустой ввод.")
            continue

        result = system.execute_minimization_pipeline(user_input)

        if "error" in result:
            print(f"Ошибка: {result['error']}")
        else:
            print("\n" + "РЕЗУЛЬТАТЫ МИНИМИЗАЦИИ:")
            print(result["formatted_output"])


if __name__ == "__main__":
    main()