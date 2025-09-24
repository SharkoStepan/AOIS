import re
from typing import Dict, List, Tuple


class LogicalExpressionProcessor:
    def __init__(self):
        self.supported_operators = {'&', '|', '!', '->', '~'}
        self.supported_variables = {'a', 'b', 'c', 'd', 'e'}
        self.operator_precedence = {'!': 5, '~': 4, '&': 3, '|': 2, '->': 1}

    def validate_and_parse(self, expression: str) -> Dict:
        """Комплексная валидация и парсинг логического выражения"""
        # Очистка от пробелов
        cleaned_expression = self._remove_whitespace(expression)

        # Базовая валидация
        validation_result = self._validate_expression(cleaned_expression)
        if not validation_result["is_valid"]:
            return validation_result

        # Извлечение переменных
        variables = self._extract_unique_variables(cleaned_expression)

        # Токенизация
        tokens = self._tokenize_expression(cleaned_expression)
        if not tokens:
            return {"is_valid": False, "error_message": "Ошибка токенизации"}

        # Преобразование в постфиксную форму
        postfix_tokens = self._convert_to_postfix(tokens)

        return {
            "is_valid": True,
            "original_expression": expression,
            "cleaned_expression": cleaned_expression,
            "variables": variables,
            "tokens": tokens,
            "postfix_tokens": postfix_tokens
        }

    def _remove_whitespace(self, expression: str) -> str:
        """Удаление всех пробельных символов"""
        return re.sub(r'\s+', '', expression)

    def _validate_expression(self, expression: str) -> Dict:
        """Комплексная валидация выражения"""
        # Удаляем пробелы перед валидацией
        expression = self._remove_whitespace(expression)

        if not expression:
            return {"is_valid": False, "error_message": "Пустое выражение"}

        # Проверка символов
        if not self._validate_characters(expression):
            return {"is_valid": False, "error_message": "Недопустимые символы в выражении"}

        # Проверка скобок
        if not self._validate_parentheses(expression):
            return {"is_valid": False, "error_message": "Несбалансированные скобки"}

        # Проверка синтаксиса
        syntax_error = self._validate_syntax(expression)
        if syntax_error:
            return {"is_valid": False, "error_message": syntax_error}

        return {"is_valid": True}

    def _validate_characters(self, expression: str) -> bool:
        """Проверка допустимости символов"""
        pattern = r'^[a-e&|!~()\->]+$'
        if not re.match(pattern, expression):
            return False
        return True

    def _validate_parentheses(self, expression: str) -> bool:
        """Проверка баланса скобок"""
        balance = 0
        for char in expression:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    def _validate_syntax(self, expression: str) -> str:
        """Проверка синтаксической корректности (улучшенная версия)"""
        # Проверка операторов в начале/конце
        if expression[0] in {'&', '|', '~', '->'}:
            return "Выражение не может начинаться с бинарного оператора"
        if expression[-1] in {'&', '|', '~', '-', '!'}:
            return "Выражение не может заканчиваться оператором"

        # Проверка пустых скобок
        if '()' in expression:
            return "Пустые скобки"

        # Проверка последовательности операторов
        if re.search(r'[&|~!]{2,}', expression):
            return "Некорректная последовательность операторов"

        # Проверка импликации
        if re.search(r'->.*->', expression):
            return "Некорректное использование импликации"

        return ""

    def _extract_unique_variables(self, expression: str) -> List[str]:
        """Извлечение уникальных переменных в алфавитном порядке"""
        variables = sorted(set(char for char in expression if char in self.supported_variables))
        return variables

    def _tokenize_expression(self, expression: str) -> List[str]:
        """Токенизация выражения"""
        tokens = []
        i = 0
        n = len(expression)

        while i < n:
            if expression[i] in self.supported_variables:
                tokens.append(expression[i])
                i += 1
            elif expression[i] in {'(', ')', '!', '&', '|', '~'}:
                tokens.append(expression[i])
                i += 1
            elif expression[i] == '-' and i + 1 < n and expression[i + 1] == '>':
                tokens.append('->')
                i += 2
            else:
                return []
        return tokens

    def _convert_to_postfix(self, tokens: List[str]) -> List[str]:
        """Преобразование в постфиксную нотацию (алгоритм сортировочной станции)"""
        output = []
        operator_stack = []

        for token in tokens:
            if token in self.supported_variables:
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                operator_stack.pop()  # Удаляем '('
            elif token in self.operator_precedence:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       self.operator_precedence.get(operator_stack[-1], 0) >= self.operator_precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            output.append(operator_stack.pop())

        return output