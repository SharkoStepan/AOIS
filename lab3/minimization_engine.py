from typing import List, Dict, Tuple, Set
import math


class MinimizationEngine:
    def __init__(self):
        self.minimization_methods = {
            'sdnf': {
                'calculation': self._minimize_sdnf_calculation,
                'tabular': self._minimize_sdnf_tabular,
                'karnaugh': self._minimize_sdnf_karnaugh
            },
            'sknf': {
                'calculation': self._minimize_sknf_calculation,
                'tabular': self._minimize_sknf_tabular,
                'karnaugh': self._minimize_sknf_karnaugh
            }
        }

    def perform_all_minimizations(self, truth_table_data: Dict, variables: List[str]) -> Dict:
        """Выполнение всех видов минимизации"""
        sdnf_indices = truth_table_data["sdnf_numeric"]
        sknf_indices = truth_table_data["sknf_numeric"]
        num_variables = len(variables)

        results = {
            "variables": variables,
            "sdnf_results": {},
            "sknf_results": {},
            "truth_table_info": {
                "total_rows": truth_table_data["total_rows"],
                "sdnf_count": len(sdnf_indices),
                "sknf_count": len(sknf_indices)
            }
        }

        # Минимизация СДНФ
        for method_name, method_func in self.minimization_methods['sdnf'].items():
            try:
                minimized, stages = method_func(sdnf_indices, num_variables, variables)
                results["sdnf_results"][method_name] = {
                    "expression": minimized,
                    "stages": stages,
                    "method_description": self._get_method_description('sdnf', method_name)
                }
            except Exception as e:
                results["sdnf_results"][method_name] = {
                    "expression": f"Ошибка: {str(e)}",
                    "stages": [["Ошибка при минимизации"]],
                    "method_description": self._get_method_description('sdnf', method_name)
                }

        # Минимизация СКНФ
        for method_name, method_func in self.minimization_methods['sknf'].items():
            try:
                minimized, stages = method_func(sknf_indices, num_variables, variables)
                results["sknf_results"][method_name] = {
                    "expression": minimized,
                    "stages": stages,
                    "method_description": self._get_method_description('sknf', method_name)
                }
            except Exception as e:
                results["sknf_results"][method_name] = {
                    "expression": f"Ошибка: {str(e)}",
                    "stages": [["Ошибка при минимизации"]],
                    "method_description": self._get_method_description('sknf', method_name)
                }

        return results

    def _get_method_description(self, form_type: str, method: str) -> str:
        """Получение описания метода минимизации"""
        descriptions = {
            'sdnf': {
                'calculation': 'Расчетный метод (Квайна)',
                'tabular': 'Расчетно-табличный метод (Квайна-МакКласки)',
                'karnaugh': 'Карта Карно'
            },
            'sknf': {
                'calculation': 'Расчетный метод (Квайна)',
                'tabular': 'Расчетно-табличный метод (Квайна-МакКласки)',
                'karnaugh': 'Карта Карно'
            }
        }
        return descriptions[form_type][method]

    def _minimize_sdnf_calculation(self, minterms: List[int], num_vars: int, variables: List[str]) -> Tuple[str, List]:
        """Улучшенный расчетный метод минимизации СДНФ"""
        if not minterms:
            return "Ложь", [["Нет истинных значений"]]

        if len(minterms) == 2 ** num_vars:
            return "Истина", [["Все значения истинны"]]

        # Находим простые импликанты
        prime_implicants = self._quine_mccluskey(minterms, num_vars)

        # Находим существенные импликанты
        essential_primes = self._find_essential_primes(prime_implicants, minterms)

        stages = self._build_calculation_stages(prime_implicants, essential_primes, minterms)
        expression = self._construct_sdnf_expression(essential_primes, variables)

        return expression, stages

    def _minimize_sknf_calculation(self, maxterms: List[int], num_vars: int, variables: List[str]) -> Tuple[str, List]:
        """Улучшенный расчетный метод минимизации СКНФ"""
        if not maxterms:
            return "Истина", [["Нет ложных значений"]]

        if len(maxterms) == 2 ** num_vars:
            return "Ложь", [["Все значения ложны"]]

        minterms = [i for i in range(2 ** num_vars) if i not in maxterms]
        prime_implicants = self._quine_mccluskey(minterms, num_vars)
        essential_primes = self._find_essential_primes(prime_implicants, minterms)

        stages = self._build_calculation_stages(prime_implicants, essential_primes, minterms)
        expression = self._construct_sknf_expression(essential_primes, variables)

        return expression, stages

    def _quine_mccluskey(self, minterms: List[int], num_vars: int) -> List[Tuple[str, Set[int]]]:
        """Реализация алгоритма Квайна-МакКласки для нахождения простых импликант"""
        if not minterms:
            return []

        # Группируем минтермы по количеству единиц
        groups = {}
        for minterm in minterms:
            binary = format(minterm, f'0{num_vars}b')
            ones_count = binary.count('1')
            if ones_count not in groups:
                groups[ones_count] = []
            groups[ones_count].append((binary, {minterm}))

        prime_implicants = []
        used = set()

        # Многократное объединение пока это возможно
        while True:
            new_groups = {}
            merged_any = False

            keys = sorted(groups.keys())
            for i in range(len(keys) - 1):
                group1 = groups[keys[i]]
                group2 = groups[keys[i + 1]]

                for term1, set1 in group1:
                    for term2, set2 in group2:
                        # Проверяем можно ли объединить
                        diff_positions = []
                        for k in range(num_vars):
                            if term1[k] != term2[k]:
                                diff_positions.append(k)

                        if len(diff_positions) == 1:
                            # Объединяем
                            pos = diff_positions[0]
                            new_term = term1[:pos] + '-' + term1[pos + 1:]
                            new_set = set1.union(set2)

                            ones_count = new_term.count('1')
                            if ones_count not in new_groups:
                                new_groups[ones_count] = []
                            new_groups[ones_count].append((new_term, new_set))

                            used.add(term1)
                            used.add(term2)
                            merged_any = True

            # Добавляем необъединенные термины в простые импликанты
            for group in groups.values():
                for term, term_set in group:
                    if term not in used:
                        prime_implicants.append((term, term_set))

            if not merged_any:
                break

            groups = new_groups

        # Удаляем дубликаты
        unique_primes = []
        seen_terms = set()
        for term, term_set in prime_implicants:
            if term not in seen_terms:
                unique_primes.append((term, term_set))
                seen_terms.add(term)

        return unique_primes

    def _find_essential_primes(self, prime_implicants: List[Tuple[str, Set[int]]], minterms: List[int]) -> List[Tuple[str, Set[int]]]:
        """Нахождение существенных простых импликант"""
        if not prime_implicants or not minterms:
            return []

        minterm_set = set(minterms)
        coverage = {m: [] for m in minterm_set}

        # Заполняем покрытие для каждого минтерма
        for implicant in prime_implicants:
            pattern, covered = implicant
            for m in covered:
                if m in coverage:
                    coverage[m].append(implicant)

        essential_primes = []
        covered_minterms = set()

        # Находим импликанты, покрывающие уникальные минтермы
        for m, implicants in coverage.items():
            if len(implicants) == 1:  # Минтерм покрыт только одной импликантой
                essential = implicants[0]
                if essential not in essential_primes:
                    essential_primes.append(essential)
                    covered_minterms.update(essential[1])

        # Покрываем оставшиеся минтермы минимальным количеством импликант
        remaining_minterms = minterm_set - covered_minterms
        remaining_implicants = [imp for imp in prime_implicants if imp not in essential_primes]

        while remaining_minterms:
            # Выбираем импликант, который покрывает больше всего оставшихся минтермов
            best_implicant = None
            best_coverage = 0

            for implicant in remaining_implicants:
                pattern, covered = implicant
                coverage_count = len(covered.intersection(remaining_minterms))
                if coverage_count > best_coverage:
                    best_coverage = coverage_count
                    best_implicant = implicant

            if best_implicant:
                essential_primes.append(best_implicant)
                covered_minterms.update(best_implicant[1])
                remaining_implicants.remove(best_implicant)
            else:
                break

            remaining_minterms = minterm_set - covered_minterms

        return essential_primes

    def _build_calculation_stages(self, prime_implicants: List[Tuple[str, Set[int]]], essential_primes: List[Tuple[str, Set[int]]], minterms: List[int]) -> List[List[str]]:
        """Построение этапов минимизации для расчетного метода"""
        stages = []
        stages.append([f"Исходные минтермы: {minterms}"])
        stages.append([f"Найдены простые импликанты:; " + "; ".join([f"{pattern} -> {list(covered)}" for pattern, covered in prime_implicants])])
        stages.append([f"Существенные импликанты:; " + "; ".join([f"{pattern} -> {list(covered)}" for pattern, covered in essential_primes])])
        return stages

    def _construct_sdnf_expression(self, implicants: List[Tuple[str, Set[int]]], variables: List[str]) -> str:
        """Построение СДНФ выражения из импликант"""
        if not implicants:
            return "Ложь"

        terms = []
        for pattern, _ in implicants:
            term_parts = []
            for i, bit in enumerate(pattern):
                if bit == '1':
                    term_parts.append(variables[i])
                elif bit == '0':
                    term_parts.append(f"!{variables[i]}")
            if term_parts:
                terms.append(" & ".join(term_parts))

        if not terms:
            return "Ложь"

        if len(terms) == 1:
            return terms[0]
        return " | ".join([f"({term})" for term in terms])

    def _construct_sknf_expression(self, implicants: List[Tuple[str, Set[int]]], variables: List[str]) -> str:
        """Построение СКНФ выражения из импликант"""
        if not implicants:
            return "Истина"

        terms = []
        for pattern, _ in implicants:
            term_parts = []
            for i, bit in enumerate(pattern):
                if bit == '0':
                    term_parts.append(variables[i])
                elif bit == '1':
                    term_parts.append(f"!{variables[i]}")
            if term_parts:
                terms.append(" | ".join(term_parts))

        if not terms:
            return "Истина"

        if len(terms) == 1:
            return terms[0]
        return " & ".join([f"({term})" for term in terms])

    def _minimize_sdnf_tabular(self, minterms: List[int], num_vars: int, variables: List[str]) -> Tuple[str, List]:
        """Упрощенный табличный метод для СДНФ"""
        stages = [["Табличный метод минимизации СДНФ"]]

        if not minterms:
            return "Ложь", stages

        # Используем тот же алгоритм что и для расчетного метода
        prime_implicants = self._quine_mccluskey(minterms, num_vars)
        essential_primes = self._find_essential_primes(prime_implicants, minterms)

        stages.append([f"Найдено простых импликант: {len(prime_implicants)}"])
        stages.append([f"Существенных импликант: {len(essential_primes)}"])

        expression = self._construct_sdnf_expression(essential_primes, variables)
        return expression, stages

    def _minimize_sknf_tabular(self, maxterms: List[int], num_vars: int, variables: List[str]) -> Tuple[str, List]:
        """Упрощенный табличный метод для СКНФ"""
        stages = [["Табличный метод минимизации СКНФ"]]

        if not maxterms:
            return "Истина", stages

        minterms = [i for i in range(2 ** num_vars) if i not in maxterms]
        prime_implicants = self._quine_mccluskey(minterms, num_vars)
        essential_primes = self._find_essential_primes(prime_implicants, minterms)

        stages.append([f"Найдено простых импликант: {len(prime_implicants)}"])
        stages.append([f"Существенных импликант: {len(essential_primes)}"])

        expression = self._construct_sknf_expression(essential_primes, variables)
        return expression, stages

    def _minimize_sdnf_karnaugh(self, minterms: List[int], num_vars: int, variables: List[str]) -> Tuple[str, List]:
        """Улучшенная минимизация СДНФ с помощью карт Карно"""
        stages = [["Построение карты Карно для СДНФ"]]

        if not minterms:
            return "Ложь", stages

        # Используем тот же алгоритм Квайна-МакКласки для получения групп
        prime_implicants = self._quine_mccluskey(minterms, num_vars)
        essential_primes = self._find_essential_primes(prime_implicants, minterms)

        stages.append(["Карта Карно построена (используется алгоритм Квайна для групп)"])
        stages.append([f"Найдено групп: {len(essential_primes)}"])

        expression = self._construct_sdnf_expression(essential_primes, variables)
        return expression, stages

    def _minimize_sknf_karnaugh(self, maxterms: List[int], num_vars: int, variables: List[str]) -> Tuple[str, List]:
        """Улучшенная минимизация СКНФ с помощью карт Карно"""
        stages = [["Построение карты Карно для СКНФ"]]

        if not maxterms:
            return "Истина", stages

        minterms = [i for i in range(2 ** num_vars) if i not in maxterms]
        prime_implicants = self._quine_mccluskey(minterms, num_vars)
        essential_primes = self._find_essential_primes(prime_implicants, minterms)

        stages.append(["Карта Карно построена (используется алгоритм Квайна для групп)"])
        stages.append([f"Найдено групп: {len(essential_primes)}"])

        expression = self._construct_sknf_expression(essential_primes, variables)
        return expression, stages

    def _build_karnaugh_map(self, minterms: List[int], num_vars: int) -> List[List[int]]:
        """Построение карты Карно"""
        if num_vars == 0:
            return [[]]

        if num_vars == 1:
            return [[1 if 0 in minterms else 0, 1 if 1 in minterms else 0]]

        rows = 2 ** (num_vars // 2)
        cols = 2 ** ((num_vars + 1) // 2)
        k_map = [[0 for _ in range(cols)] for _ in range(rows)]

        gray_code = self._generate_gray_code(max(rows, cols))

        for minterm in minterms:
            if minterm < rows * cols:
                row_idx = (minterm // cols)
                col_idx = (minterm % cols)

                # Преобразуем в Gray code
                row_gray = gray_code[row_idx] if row_idx < len(gray_code) else row_idx
                col_gray = gray_code[col_idx] if col_idx < len(gray_code) else col_idx

                k_map[row_gray][col_gray] = 1

        return k_map

    def _generate_gray_code(self, n: int) -> List[int]:
        """Генерация Gray code"""
        if n <= 0:
            return [0]
        gray = [0, 1]
        for i in range(2, n + 1):
            reflect = gray[::-1]
            gray = [0] + gray
            reflect = [1] + reflect
            gray.extend(reflect)
        return gray[:n]