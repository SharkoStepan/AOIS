from typing import List, Dict, Any


class TruthTableGenerator:
    def __init__(self):
        self.logical_operations = {
            '!': lambda a: not a,
            '&': lambda a, b: a and b,
            '|': lambda a, b: a or b,
            '->': lambda a, b: (not a) or b,
            '~': lambda a, b: a == b
        }

    def generate_complete_table(self, variables: List[str], postfix_tokens: List[str]) -> Dict[str, Any]:
        """Генерация полной таблицы истинности с дополнительной информацией"""
        # Убрана оптимизация, т.к. она ломает сложные выражения; evaluate_postfix handles все операторы напрямую
        optimized_tokens = postfix_tokens
        truth_table = self._compute_truth_table(variables, optimized_tokens)

        return {
            "variables": variables,
            "truth_table": truth_table,
            "sdnf_numeric": self._extract_sdnf_indices(truth_table),
            "sknf_numeric": self._extract_sknf_indices(truth_table),
            "total_rows": len(truth_table)
        }

    def _optimize_expression(self, postfix_tokens: List[str]) -> List[str]:
        """Простая оптимизация выражения перед вычислением — отключена, возвращаем как есть"""
        return postfix_tokens

    def _compute_truth_table(self, variables: List[str], postfix_tokens: List[str]) -> List[Dict]:
        """Вычисление таблицы истинности"""
        num_variables = len(variables)
        table_size = 2 ** num_variables
        truth_table = []

        for row_index in range(table_size):
            variable_values = self._generate_variable_combination(variables, row_index, num_variables)
            result = self._evaluate_postfix(postfix_tokens, variable_values)

            table_row = {
                "row_index": row_index,
                "variable_values": variable_values.copy(),
                "result": result,
                "binary_representation": self._get_binary_representation(row_index, num_variables)
            }
            truth_table.append(table_row)

        return truth_table

    def _generate_variable_combination(self, variables: List[str], row_index: int, num_vars: int) -> Dict[str, bool]:
        """Генерация комбинации значений переменных для строки таблицы"""
        values = {}
        for i, variable in enumerate(variables):
            bit_position = num_vars - 1 - i
            values[variable] = bool((row_index >> bit_position) & 1)
        return values

    def _get_binary_representation(self, number: int, length: int) -> str:
        """Получение двоичного представления числа"""
        return format(number, f'0{length}b')

    def _evaluate_postfix(self, postfix_tokens: List[str], variable_values: Dict[str, bool]) -> bool:
        """Вычисление значения выражения в постфиксной записи"""
        evaluation_stack = []

        for token in postfix_tokens:
            if token in variable_values:
                evaluation_stack.append(variable_values[token])
            elif token in self.logical_operations:
                operation = self.logical_operations[token]
                if token == '!':
                    if len(evaluation_stack) < 1:
                        raise ValueError("Недостаточно операндов для унарной операции")
                    operand = evaluation_stack.pop()
                    result = operation(operand)
                    evaluation_stack.append(result)
                else:
                    if len(evaluation_stack) < 2:
                        raise ValueError(f"Недостаточно операндов для бинарной операции '{token}'")
                    operand2 = evaluation_stack.pop()
                    operand1 = evaluation_stack.pop()
                    result = operation(operand1, operand2)
                    evaluation_stack.append(result)
            else:
                raise ValueError(f"Неизвестный токен: {token}")

        if len(evaluation_stack) != 1:
            raise ValueError(f"Некорректное выражение. Осталось значений в стеке: {len(evaluation_stack)}")

        return evaluation_stack[0]

    def _extract_sdnf_indices(self, truth_table: List[Dict]) -> List[int]:
        """Извлечение индексов строк где функция истинна (для СДНФ)"""
        return [row["row_index"] for row in truth_table if row["result"]]

    def _extract_sknf_indices(self, truth_table: List[Dict]) -> List[int]:
        """Извлечение индексов строк где функция ложна (для СКНФ)"""
        return [row["row_index"] for row in truth_table if not row["result"]]

    def get_truth_table_display(self, truth_table_data: Dict) -> List[str]:
        """Форматирование таблицы истинности для отображения"""
        if not truth_table_data or "truth_table" not in truth_table_data:
            return ["Таблица истинности недоступна"]

        truth_table = truth_table_data["truth_table"]
        variables = truth_table_data["variables"]

        # Создаем заголовок
        header = variables + ["F"]
        display_lines = []

        # Добавляем заголовок
        header_line = " | ".join(f"{var:^3}" for var in header)
        separator = "-" * len(header_line)
        display_lines.append(header_line)
        display_lines.append(separator)

        # Добавляем строки таблицы
        for row in truth_table:
            var_values = [str(int(row["variable_values"][var])) for var in variables]
            result_value = str(int(row["result"]))
            row_line = " | ".join(f"{val:^3}" for val in var_values + [result_value])
            display_lines.append(row_line)

        return display_lines

    def get_minterm_maxterm_info(self, truth_table_data: Dict) -> Dict[str, Any]:
        """Получение информации о минтермах и макстермах"""
        sdnf_indices = truth_table_data["sdnf_numeric"]
        sknf_indices = truth_table_data["sknf_numeric"]
        variables = truth_table_data["variables"]
        num_vars = len(variables)

        # Формируем текстовое представление СДНФ и СКНФ
        sdnf_terms = []
        for idx in sdnf_indices:
            binary = format(idx, f'0{num_vars}b')
            term_parts = []
            for i, bit in enumerate(binary):
                if bit == '1':
                    term_parts.append(variables[i])
                else:
                    term_parts.append(f"!{variables[i]}")
            sdnf_terms.append(" & ".join(term_parts))

        sknf_terms = []
        for idx in sknf_indices:
            binary = format(idx, f'0{num_vars}b')
            clause_parts = []
            for i, bit in enumerate(binary):
                if bit == '0':
                    clause_parts.append(variables[i])
                else:
                    clause_parts.append(f"!{variables[i]}")
            sknf_terms.append(" | ".join(clause_parts))

        return {
            "sdnf_expression": " | ".join([f"({term})" for term in sdnf_terms]) if sdnf_terms else "Ложь",
            "sknf_expression": " & ".join([f"({clause})" for clause in sknf_terms]) if sknf_terms else "Истина",
            "sdnf_numeric": sdnf_indices,
            "sknf_numeric": sknf_indices,
            "sdnf_count": len(sdnf_indices),
            "sknf_count": len(sknf_indices)
        }