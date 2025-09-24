from typing import Dict, List


class ResultsPresenter:
    def __init__(self):
        self.section_separator = "=" * 60
        self.subsection_separator = "-" * 40

    def format_comprehensive_results(self, minimization_results: Dict) -> Dict[str, str]:
        """Форматирование комплексных результатов минимизации"""
        output_lines = []

        # Заголовок
        output_lines.append("АНАЛИЗ ЛОГИЧЕСКОЙ ФУНКЦИИ")
        output_lines.append(self.section_separator)

        # ТАБЛИЦА ИСТИННОСТИ
        if "truth_table_display" in minimization_results:
            output_lines.extend(self._format_truth_table(minimization_results))
            output_lines.append(self.subsection_separator)

        # Информация о функции
        output_lines.extend(self._format_function_info(minimization_results))
        output_lines.append(self.subsection_separator)

        # Результаты СДНФ
        output_lines.extend(self._format_sdnf_results(minimization_results))
        output_lines.append(self.subsection_separator)

        # Результаты СКНФ
        output_lines.extend(self._format_sknf_results(minimization_results))
        output_lines.append(self.section_separator)

        formatted_output = "\n".join(output_lines)

        return {
            "formatted_output": formatted_output,
            "raw_data": minimization_results
        }

    def _format_truth_table(self, results: Dict) -> List[str]:
        """Форматирование таблицы истинности для вывода"""
        if "truth_table_display" not in results:
            return []

        table_lines = ["📋 ТАБЛИЦА ИСТИННОСТИ:"]
        table_lines.extend(results["truth_table_display"])
        return table_lines

    def _format_function_info(self, results: Dict) -> List[str]:
        """Форматирование информации о логической функции"""
        info_lines = [
            "📊 ИНФОРМАЦИЯ О ФУНКЦИИ:",
            f"Переменные: {', '.join(results['variables'])}",
            f"Общее число комбинаций: {results['truth_table_info']['total_rows']}",
            f"Число истинных значений (для СДНФ): {results['truth_table_info']['sdnf_count']}",
            f"Число ложных значений (для СКНФ): {results['truth_table_info']['sknf_count']}"
        ]

        # Добавляем информацию о СДНФ и СКНФ если есть
        if "minterm_info" in results:
            info_lines.append(f"СДНФ: {results['minterm_info']['sdnf_expression']}")
            info_lines.append(f"СКНФ: {results['minterm_info']['sknf_expression']}")

        return info_lines

    def _format_sdnf_results(self, results: Dict) -> List[str]:
        """Форматирование результатов минимизации СДНФ"""
        sdnf_lines = ["🎯 МИНИМИЗАЦИЯ СДНФ:"]

        for method_name, method_data in results['sdnf_results'].items():
            sdnf_lines.extend([
                f"▸ {method_data['method_description']}:",
                f"  Результат: {method_data['expression']}",
                f"  Этапы: {len(method_data['stages'])} этапов"
            ])

            # Добавление подробностей этапов (только первые 3 этапа для краткости)
            for i, stage in enumerate(method_data['stages'][:3], 1):
                stage_text = "; ".join(stage) if isinstance(stage, list) else str(stage)
                if len(stage_text) <= 100:  # Ограничиваем длину вывода
                    sdnf_lines.append(f"    Этап {i}: {stage_text}")

            sdnf_lines.append("")  # Пустая строка между методами

        return sdnf_lines

    def _format_sknf_results(self, results: Dict) -> List[str]:
        """Форматирование результатов минимизации СКНФ"""
        sknf_lines = ["🎯 МИНИМИЗАЦИЯ СКНФ:"]

        for method_name, method_data in results['sknf_results'].items():
            sknf_lines.extend([
                f"▸ {method_data['method_description']}:",
                f"  Результат: {method_data['expression']}",
                f"  Этапы: {len(method_data['stages'])} этапов"
            ])

            # Добавление подробностей этапов
            for i, stage in enumerate(method_data['stages'][:3], 1):
                stage_text = "; ".join(stage) if isinstance(stage, list) else str(stage)
                if len(stage_text) <= 100:
                    sknf_lines.append(f"    Этап {i}: {stage_text}")

            sknf_lines.append("")
        return sknf_lines

    def format_error_message(self, error_data: Dict) -> str:
        """Форматирование сообщения об ошибке"""
        error_type = error_data.get('type', 'UNKNOWN_ERROR')
        message = error_data.get('message', 'Неизвестная ошибка')

        error_messages = {
            'SYNTAX_ERROR': f"Синтаксическая ошибка: {message}",
            'VALIDATION_ERROR': f"Ошибка валидации: {message}",
            'EVALUATION_ERROR': f"Ошибка вычисления: {message}",
            'UNKNOWN_ERROR': f"Неизвестная ошибка: {message}"
        }

        return error_messages.get(error_type, f"Ошибка: {message}")