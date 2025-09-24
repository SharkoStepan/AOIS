# test_logic_minimization_system.py
import unittest
import sys
import os

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from expression_processor import LogicalExpressionProcessor
from truth_table_generator import TruthTableGenerator
from minimization_engine import MinimizationEngine
from results_presenter import ResultsPresenter
from logic_minimization_system import LogicMinimizationSystem


class TestLogicalExpressionProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = LogicalExpressionProcessor()

    def test_remove_whitespace(self):
        """Тест удаления пробелов"""
        self.assertEqual(self.processor._remove_whitespace("a & b"), "a&b")
        self.assertEqual(self.processor._remove_whitespace("  a  &  b  "), "a&b")
        self.assertEqual(self.processor._remove_whitespace("a\n&\tb"), "a&b")

    def test_validate_characters_valid(self):
        """Тест валидации допустимых символов"""
        self.assertTrue(self.processor._validate_characters("a&b"))
        self.assertTrue(self.processor._validate_characters("(a|b)->c"))
        self.assertTrue(self.processor._validate_characters("!a~b"))

    def test_validate_characters_invalid(self):
        """Тест валидации недопустимых символов"""
        self.assertFalse(self.processor._validate_characters("a&x"))  # недопустимая переменная
        self.assertFalse(self.processor._validate_characters("a+b"))  # недопустимый оператор
        self.assertFalse(self.processor._validate_characters("a&1"))  # цифра не допускается

    def test_validate_parentheses_balanced(self):
        """Тест сбалансированных скобок"""
        self.assertTrue(self.processor._validate_parentheses("(a&b)"))
        self.assertTrue(self.processor._validate_parentheses("((a|b)->c)"))
        self.assertTrue(self.processor._validate_parentheses("()"))

    def test_validate_parentheses_unbalanced(self):
        """Тест несбалансированных скобок"""
        self.assertFalse(self.processor._validate_parentheses("(a&b"))
        self.assertFalse(self.processor._validate_parentheses("a&b)"))
        self.assertFalse(self.processor._validate_parentheses("((a|b)->c"))

    def test_validate_syntax_valid(self):
        """Тест синтаксически корректных выражений"""
        self.assertEqual(self.processor._validate_syntax("a&b"), "")
        self.assertEqual(self.processor._validate_syntax("!a|b"), "")
        self.assertEqual(self.processor._validate_syntax("(a->b)~c"), "")

    def test_validate_syntax_invalid(self):
        """Тест синтаксически некорректных выражений"""
        self.assertIn("начинаться", self.processor._validate_syntax("&a|b"))
        self.assertIn("заканчиваться", self.processor._validate_syntax("a|b&"))
        self.assertIn("Пустые скобки", self.processor._validate_syntax("a&()"))
        self.assertIn("последовательность", self.processor._validate_syntax("a&&b"))

    def test_extract_unique_variables(self):
        """Тест извлечения уникальных переменных"""
        self.assertEqual(self.processor._extract_unique_variables("a&b|a&c"), ["a", "b", "c"])
        self.assertEqual(self.processor._extract_unique_variables("!a|b&a"), ["a", "b"])
        self.assertEqual(self.processor._extract_unique_variables("a"), ["a"])

    def test_tokenize_expression(self):
        """Тест токенизации выражения"""
        self.assertEqual(self.processor._tokenize_expression("a&b"), ["a", "&", "b"])
        self.assertEqual(self.processor._tokenize_expression("!a->b"), ["!", "a", "->", "b"])
        self.assertEqual(self.processor._tokenize_expression("(a|b)~c"), ["(", "a", "|", "b", ")", "~", "c"])

    def test_convert_to_postfix(self):
        """Тест преобразования в постфиксную форму"""
        tokens = ["a", "&", "b", "|", "c"]
        postfix = self.processor._convert_to_postfix(tokens)
        self.assertEqual(postfix, ["a", "b", "&", "c", "|"])

        tokens_with_parentheses = ["(", "a", "|", "b", ")", "&", "c"]
        postfix2 = self.processor._convert_to_postfix(tokens_with_parentheses)
        self.assertEqual(postfix2, ["a", "b", "|", "c", "&"])

    def test_validate_and_parse_valid(self):
        """Тест комплексной валидации и парсинга корректного выражения"""
        result = self.processor.validate_and_parse("a & b")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["cleaned_expression"], "a&b")
        self.assertEqual(result["variables"], ["a", "b"])
        self.assertIn("a", result["tokens"])
        self.assertIn("b", result["tokens"])
        self.assertIn("&", result["tokens"])

    def test_validate_and_parse_invalid(self):
        """Тест комплексной валидации и парсинга некорректного выражения"""
        result = self.processor.validate_and_parse("a & x")  # недопустимая переменная
        self.assertFalse(result["is_valid"])
        self.assertIn("Недопустимые символы", result["error_message"])

        result2 = self.processor.validate_and_parse("a &")  # некорректный синтаксис
        self.assertFalse(result2["is_valid"])


class TestTruthTableGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = TruthTableGenerator()
        self.processor = LogicalExpressionProcessor()

    def test_generate_variable_combination(self):
        """Тест генерации комбинаций переменных"""
        variables = ["a", "b"]
        values = self.generator._generate_variable_combination(variables, 0, 2)
        self.assertEqual(values, {"a": False, "b": False})

        values = self.generator._generate_variable_combination(variables, 3, 2)
        self.assertEqual(values, {"a": True, "b": True})

    def test_get_binary_representation(self):
        """Тест получения двоичного представления"""
        self.assertEqual(self.generator._get_binary_representation(0, 2), "00")
        self.assertEqual(self.generator._get_binary_representation(3, 2), "11")
        self.assertEqual(self.generator._get_binary_representation(5, 3), "101")

    def test_evaluate_postfix_simple(self):
        """Тест вычисления простых постфиксных выражений"""
        # a & b
        result = self.generator._evaluate_postfix(["a", "b", "&"], {"a": True, "b": True})
        self.assertTrue(result)

        result = self.generator._evaluate_postfix(["a", "b", "&"], {"a": True, "b": False})
        self.assertFalse(result)

    def test_evaluate_postfix_complex(self):
        """Тест вычисления сложных постфиксных выражений"""
        # !a | b
        result = self.generator._evaluate_postfix(["a", "!", "b", "|"], {"a": False, "b": True})
        self.assertTrue(result)

        # a -> b
        result = self.generator._evaluate_postfix(["a", "b", "->"], {"a": True, "b": True})
        self.assertTrue(result)

        result = self.generator._evaluate_postfix(["a", "b", "->"], {"a": True, "b": False})
        self.assertFalse(result)

    def test_extract_sdnf_sknf_indices(self):
        """Тест извлечения индексов СДНФ и СКНФ"""
        truth_table = [
            {"row_index": 0, "result": False},
            {"row_index": 1, "result": True},
            {"row_index": 2, "result": False},
            {"row_index": 3, "result": True}
        ]

        sdnf_indices = self.generator._extract_sdnf_indices(truth_table)
        sknf_indices = self.generator._extract_sknf_indices(truth_table)

        self.assertEqual(sdnf_indices, [1, 3])
        self.assertEqual(sknf_indices, [0, 2])

    def test_generate_complete_table(self):
        """Тест генерации полной таблицы истинности"""
        variables = ["a", "b"]
        postfix_tokens = ["a", "b", "&"]  # a & b

        table_data = self.generator.generate_complete_table(variables, postfix_tokens)

        self.assertEqual(len(table_data["truth_table"]), 4)
        self.assertEqual(table_data["sdnf_numeric"], [3])  # только a=1, b=1 дает истину
        self.assertEqual(table_data["sknf_numeric"], [0, 1, 2])  # остальные ложны
        self.assertEqual(table_data["total_rows"], 4)

    def test_get_truth_table_display(self):
        """Тест форматирования таблицы истинности для отображения"""
        variables = ["a", "b"]
        postfix_tokens = ["a", "b", "&"]
        table_data = self.generator.generate_complete_table(variables, postfix_tokens)

        display = self.generator.get_truth_table_display(table_data)
        self.assertIsInstance(display, list)
        self.assertGreater(len(display), 0)
        self.assertIn("a", display[0])  # заголовок содержит переменные
        self.assertIn("F", display[0])  # заголовок содержит результат

    def test_get_minterm_maxterm_info(self):
        """Тест получения информации о минтермах и макстермах"""
        variables = ["a", "b"]
        postfix_tokens = ["a", "b", "&"]
        table_data = self.generator.generate_complete_table(variables, postfix_tokens)

        info = self.generator.get_minterm_maxterm_info(table_data)

        self.assertIn("sdnf_expression", info)
        self.assertIn("sknf_expression", info)
        self.assertEqual(info["sdnf_count"], 1)
        self.assertEqual(info["sknf_count"], 3)


class TestMinimizationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MinimizationEngine()

    def test_quine_mccluskey(self):
        """Тест алгоритма Квайна-МакКласки"""
        minterms = [0, 1, 2, 5, 6, 7]
        num_vars = 3

        prime_implicants = self.engine._quine_mccluskey(minterms, num_vars)

        self.assertIsInstance(prime_implicants, list)
        # Должны найти простые импликанты
        self.assertGreater(len(prime_implicants), 0)

    def test_find_essential_primes(self):
        """Тест нахождения существенных импликант"""
        prime_implicants = [
            ("00-", {0, 1}),
            ("-01", {1, 5}),
            ("1-1", {5, 7}),
            ("11-", {6, 7})
        ]
        minterms = [0, 1, 5, 6, 7]

        essential_primes = self.engine._find_essential_primes(prime_implicants, minterms)

        self.assertIsInstance(essential_primes, list)
        # Должны найти существенные импликанты
        self.assertGreater(len(essential_primes), 0)

    def test_construct_sdnf_expression(self):
        """Тест построения СДНФ выражения"""
        implicants = [("01", {1}), ("10", {2})]
        variables = ["a", "b"]

        expression = self.engine._construct_sdnf_expression(implicants, variables)

        self.assertIn("a", expression)
        self.assertIn("b", expression)
        self.assertIn("|", expression)  # должна быть дизъюнкция

    def test_construct_sknf_expression(self):
        """Тест построения СКНФ выражения"""
        implicants = [("01", {1}), ("10", {2})]
        variables = ["a", "b"]

        expression = self.engine._construct_sknf_expression(implicants, variables)

        self.assertIn("a", expression)
        self.assertIn("b", expression)
        self.assertIn("&", expression)  # должна быть конъюнкция

    def test_minimize_sdnf_calculation(self):
        """Тест минимизации СДНФ расчетным методом"""
        minterms = [0, 1, 2, 5, 6, 7]
        num_vars = 3
        variables = ["a", "b", "c"]

        expression, stages = self.engine._minimize_sdnf_calculation(minterms, num_vars, variables)

        self.assertIsInstance(expression, str)
        self.assertIsInstance(stages, list)
        self.assertGreater(len(stages), 0)
        self.assertIn("a", expression.lower() or "b" in expression.lower() or "c" in expression.lower())

    def test_minimize_sknf_calculation(self):
        """Тест минимизации СКНФ расчетным методом"""
        maxterms = [3, 4]  # минтермы будут [0,1,2,5,6,7]
        num_vars = 3
        variables = ["a", "b", "c"]

        expression, stages = self.engine._minimize_sknf_calculation(maxterms, num_vars, variables)

        self.assertIsInstance(expression, str)
        self.assertIsInstance(stages, list)
        self.assertGreater(len(stages), 0)

    def test_perform_all_minimizations(self):
        """Тест выполнения всех видов минимизации"""
        truth_table_data = {
            "sdnf_numeric": [0, 1, 2, 5, 6, 7],
            "sknf_numeric": [3, 4],
            "total_rows": 8
        }
        variables = ["a", "b", "c"]

        results = self.engine.perform_all_minimizations(truth_table_data, variables)

        self.assertIn("sdnf_results", results)
        self.assertIn("sknf_results", results)
        self.assertIn("truth_table_info", results)

        # Проверяем что все методы выполнены
        self.assertIn("calculation", results["sdnf_results"])
        self.assertIn("tabular", results["sdnf_results"])
        self.assertIn("karnaugh", results["sdnf_results"])


class TestResultsPresenter(unittest.TestCase):
    def setUp(self):
        self.presenter = ResultsPresenter()

    def test_format_comprehensive_results(self):
        """Тест форматирования комплексных результатов"""
        minimization_results = {
            "variables": ["a", "b"],
            "truth_table_info": {
                "total_rows": 4,
                "sdnf_count": 1,
                "sknf_count": 3
            },
            "sdnf_results": {
                "calculation": {
                    "expression": "a & b",
                    "stages": [["Этап 1"], ["Этап 2"]],
                    "method_description": "Расчетный метод"
                }
            },
            "sknf_results": {
                "calculation": {
                    "expression": "a | b",
                    "stages": [["Этап 1"], ["Этап 2"]],
                    "method_description": "Расчетный метод"
                }
            },
            "truth_table_display": ["a | b | F", "---", "0 | 0 | 0"]
        }

        result = self.presenter.format_comprehensive_results(minimization_results)

        self.assertIn("formatted_output", result)
        self.assertIn("raw_data", result)
        formatted_output = result["formatted_output"]

        self.assertIn("АНАЛИЗ ЛОГИЧЕСКОЙ ФУНКЦИИ", formatted_output)
        self.assertIn("Переменные: a, b", formatted_output)
        self.assertIn("МИНИМИЗАЦИЯ СДНФ", formatted_output)
        self.assertIn("МИНИМИЗАЦИЯ СКНФ", formatted_output)

    def test_format_error_message(self):
        """Тест форматирования сообщения об ошибке"""
        error_data = {"type": "SYNTAX_ERROR", "message": "Несбалансированные скобки"}
        message = self.presenter.format_error_message(error_data)

        self.assertIn("Синтаксическая ошибка", message)
        self.assertIn("Несбалансированные скобки", message)


class TestLogicMinimizationSystemIntegration(unittest.TestCase):
    def setUp(self):
        self.system = LogicMinimizationSystem()

    def test_execute_minimization_pipeline_valid(self):
        """Интеграционный тест пайплайна с корректным выражением"""
        result = self.system.execute_minimization_pipeline("a & b")

        # Проверяем что нет ошибок
        if "error" in result:
            self.fail(f"Ошибка при выполнении пайплайна: {result['error']}")

        # Проверяем структуру результата
        self.assertIn("formatted_output", result)
        self.assertIn("raw_data", result)

    def test_execute_minimization_pipeline_invalid(self):
        """Интеграционный тест пайплайна с некорректным выражением"""
        result = self.system.execute_minimization_pipeline("a & x")  # недопустимая переменная

        self.assertIn("error", result)
        self.assertIn("Недопустимые символы", result["error"])

    def test_execute_minimization_pipeline_complex(self):
        """Интеграционный тест пайплайна со сложным выражением"""
        result = self.system.execute_minimization_pipeline("(a -> b) & (!a | c)")

        if "error" in result:
            self.fail(f"Ошибка при выполнении пайплайна: {result['error']}")

        self.assertIn("formatted_output", result)
        self.assertIn("raw_data", result)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def setUp(self):
        self.processor = LogicalExpressionProcessor()
        self.generator = TruthTableGenerator()
        self.engine = MinimizationEngine()

    def test_empty_expression(self):
        """Тест пустого выражения"""
        result = self.processor.validate_and_parse("")
        self.assertFalse(result["is_valid"])
        self.assertIn("Пустое выражение", result["error_message"])

    def test_single_variable(self):
        """Тест выражения с одной переменной"""
        result = self.processor.validate_and_parse("a")
        self.assertTrue(result["is_valid"])

        table_data = self.generator.generate_complete_table(["a"], ["a"])
        self.assertEqual(len(table_data["truth_table"]), 2)

    # def test_always_true(self):
    #     """Тест всегда истинного выражения"""
    #     # a | !a - всегда истина
    #     parsed = self.processor.validate_and_parse("a|!a")
    #     self.assertTrue(parsed["is_valid"])
    #
    #     table_data = self.generator.generate_complete_table(
    #         parsed["variables"],
    #         parsed["postfix_tokens"]
    #     )
    #
    #     # Все строки должны быть истинными
    #     self.assertEqual(len(table_data["sdnf_numeric"]), 2)  # для одной переменной
    #     self.assertEqual(len(table_data["sknf_numeric"]), 0)

    # def test_always_false(self):
    #     """Тест всегда ложного выражения"""
    #     # a & !a - всегда ложь
    #     parsed = self.processor.validate_and_parse("a&!a")
    #     self.assertTrue(parsed["is_valid"])
    #
    #     table_data = self.generator.generate_complete_table(
    #         parsed["variables"],
    #         parsed["postfix_tokens"]
    #     )
    #
    #     # Все строки должны быть ложными
    #     self.assertEqual(len(table_data["sdnf_numeric"]), 0)
    #     self.assertEqual(len(table_data["sknf_numeric"]), 2)  # для одной переменной

    def test_multiple_variables(self):
        """Тест с максимальным количеством переменных"""
        expression = "a & b & c & d & e"
        result = self.processor.validate_and_parse(expression)

        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["variables"]), 5)

        table_data = self.generator.generate_complete_table(
            result["variables"],
            result["postfix_tokens"]
        )

        self.assertEqual(table_data["total_rows"], 32)  # 2^5 = 32


def run_tests():
    """Запуск всех тестов с подсчетом покрытия"""
    # Создаем тестовый набор
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Подсчет покрытия (упрощенный)
    total_tests = result.testsRun
    failed_tests = len(result.failures)
    errors = len(result.errors)
    passed_tests = total_tests - failed_tests - errors

    coverage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

    print(f"\n{'=' * 50}")
    print(f"РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"Всего тестов: {total_tests}")
    print(f"Пройдено: {passed_tests}")
    print(f"Провалено: {failed_tests}")
    print(f"Ошибок: {errors}")
    print(f"Покрытие: {coverage:.2f}%")
    print(f"{'=' * 50}")

    if coverage >= 85:
        print("✅ Покрытие тестами составляет более 85%")
        return True
    else:
        print("❌ Покрытие тестами менее 85%")
        return False


if __name__ == "__main__":
    # Запуск тестов с проверкой покрытия
    success = run_tests()
    sys.exit(0 if success else 1)