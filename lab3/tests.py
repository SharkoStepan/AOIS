import unittest
from unittest.mock import patch
from io import StringIO
import sys
from log_parser import *
from evaluator import *
from minimizer import *
from main import *


class TestLogicalEvaluator(unittest.TestCase):

    def test_remove_spaces(self):
        self.assertEqual(remove_spaces("a & b"), "a&b")
        self.assertEqual(remove_spaces("(a -> b)"), "(a->b)")
        self.assertEqual(remove_spaces("  a  b  c  "), "abc")
        self.assertEqual(remove_spaces(""), "")

    def test_is_valid_symbols(self):
        self.assertTrue(is_valid_symbols("a&b"))
        self.assertTrue(is_valid_symbols("a->b"))
        self.assertTrue(is_valid_symbols("!(a|b)"))
        self.assertTrue(is_valid_symbols("a&b|c->d~e"))
        self.assertFalse(is_valid_symbols("a^b"))
        self.assertFalse(is_valid_symbols("a-b"))
        self.assertFalse(is_valid_symbols("a>b"))
        self.assertFalse(is_valid_symbols("a b"))

    def test_check_parentheses(self):
        self.assertTrue(check_parentheses("(a)"))
        self.assertTrue(check_parentheses("(a|(b&c))"))
        self.assertTrue(check_parentheses("()"))
        self.assertTrue(check_parentheses("a"))
        self.assertFalse(check_parentheses("(a"))
        self.assertFalse(check_parentheses("a)"))
        self.assertFalse(check_parentheses("(a))"))
        self.assertFalse(check_parentheses("((a)"))

    def test_extract_variables(self):
        self.assertEqual(extract_variables("a&b"), ['a', 'b'])
        self.assertEqual(extract_variables("(a->b)|c"), ['a', 'b', 'c'])
        self.assertEqual(extract_variables("!a&(b|c)"), ['a', 'b', 'c'])
        self.assertEqual(extract_variables("a&a|a"), ['a'])
        self.assertEqual(extract_variables("1&0"), [])
        self.assertEqual(extract_variables(""), [])

    def test_tokenize(self):
        self.assertEqual(tokenize("a&b"), ['a', '&', 'b'])
        self.assertEqual(tokenize("a->b"), ['a', '->', 'b'])
        self.assertEqual(tokenize("!(a|b)"), ['!', '(', 'a', '|', 'b', ')'])
        self.assertEqual(tokenize("a&(b|c)"), ['a', '&', '(', 'b', '|', 'c', ')'])
        self.assertEqual(tokenize("~~a"), ['~', '~', 'a'])
        self.assertEqual(tokenize("a^b"), [])
        self.assertEqual(tokenize("a-b"), [])

    def test_shunting_yard(self):
        self.assertEqual(shunting_yard(['a', '&', 'b']), ['a', 'b', '&'])
        self.assertEqual(shunting_yard(['a', '->', 'b']), ['a', 'b', '->'])
        self.assertEqual(shunting_yard(['!', 'a']), ['a', '!'])
        self.assertEqual(shunting_yard(['(', 'a', '|', 'b', ')', '&', 'c']),
                         ['a', 'b', '|', 'c', '&'])
        self.assertEqual(shunting_yard(['a', '&', '(', 'b', '|', 'c', ')']),
                         ['a', 'b', 'c', '|', '&'])

    def test_evaluate_postfix(self):
        self.assertTrue(evaluate_postfix(['a', 'b', '&'], {'a': True, 'b': True}))
        self.assertFalse(evaluate_postfix(['a', 'b', '&'], {'a': True, 'b': False}))
        self.assertFalse(evaluate_postfix(['a', 'b', '->'], {'a': True, 'b': False}))
        self.assertTrue(evaluate_postfix(['a', 'b', '->'], {'a': False, 'b': True}))
        self.assertTrue(evaluate_postfix(['a', '!'], {'a': False}))
        self.assertFalse(evaluate_postfix(['a', '!'], {'a': True}))
        self.assertTrue(evaluate_postfix(['a', 'a', '~'], {'a': True}))
        self.assertFalse(evaluate_postfix(['a', 'b', '~'], {'a': True, 'b': False}))

    def test_generate_truth_table(self):
        variables = ['a', 'b']
        postfix = ['a', 'b', '&']
        table = generate_truth_table(variables, postfix)
        self.assertEqual(len(table), 4)
        self.assertEqual(table[0], [False, False, False])
        self.assertEqual(table[3], [True, True, True])
        variables = ['a', 'b', 'c']
        postfix = ['a', 'b', '|', 'c', '&']
        table = generate_truth_table(variables, postfix)
        self.assertEqual(len(table), 8)

    def test_generate_sdnf(self):
        variables = ['a', 'b']
        table = [
            [False, False, False],
            [False, True, True],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(generate_sdnf(variables, table), "(!a & b) | (a & b)")
        table = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, False]
        ]
        self.assertEqual(generate_sdnf(variables, table), "Always False")

    def test_generate_sknf(self):
        variables = ['a', 'b']
        table = [
            [False, False, False],
            [False, True, True],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(generate_sknf(variables, table), "(a | b) & (!a | b)")
        table = [
            [False, False, True],
            [False, True, True],
            [True, False, True],
            [True, True, True]
        ]
        self.assertEqual(generate_sknf(variables, table), "Always True")

    def test_generate_sdnf_numeric(self):
        table = [
            [False, False, False],
            [False, True, True],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(generate_sdnf_numeric(table), [1, 3])
        table = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, False]
        ]
        self.assertEqual(generate_sdnf_numeric(table), [])

    def test_generate_sknf_numeric(self):
        table = [
            [False, False, False],
            [False, True, True],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(generate_sknf_numeric(table), [0, 2])
        table = [
            [False, False, True],
            [False, True, True],
            [True, False, True],
            [True, True, True]
        ]
        self.assertEqual(generate_sknf_numeric(table), [])

    def test_generate_index_form(self):
        table = [
            [False, False, False],
            [False, True, True],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(generate_index_form(table), 5)
        table = [
            [False, False, True],
            [False, True, True],
            [True, False, False],
            [True, True, False]
        ]
        self.assertEqual(generate_index_form(table), 12)

    def test_full_pipeline(self):
        formula = "(a -> b) & c"
        formula = remove_spaces(formula)
        self.assertTrue(is_valid_symbols(formula))
        self.assertTrue(check_parentheses(formula))
        variables = extract_variables(formula)
        self.assertEqual(variables, ['a', 'b', 'c'])
        tokens = tokenize(formula)
        self.assertEqual(tokens, ['(', 'a', '->', 'b', ')', '&', 'c'])
        postfix = shunting_yard(tokens)
        self.assertEqual(postfix, ['a', 'b', '->', 'c', '&'])
        table = generate_truth_table(variables, postfix)
        self.assertEqual(len(table), 8)
        var_values = {'a': True, 'b': False, 'c': True}
        result = evaluate_postfix(postfix, var_values)
        self.assertFalse(result)

    def test_remove_spaces_edge_cases(self):
        self.assertEqual(remove_spaces("   "), "")
        self.assertEqual(remove_spaces("a"), "a")
        self.assertEqual(remove_spaces(" a "), "a")

    def test_is_valid_symbols_edge_cases(self):
        self.assertTrue(is_valid_symbols("a"))
        self.assertTrue(is_valid_symbols("!a"))
        self.assertTrue(is_valid_symbols("a|b|c"))
        self.assertFalse(is_valid_symbols("a>"))
        self.assertFalse(is_valid_symbols("-b"))

    def test_check_parentheses_edge_cases(self):
        self.assertTrue(check_parentheses(""))
        self.assertTrue(check_parentheses("()"))
        self.assertFalse(check_parentheses(")("))
        self.assertFalse(check_parentheses("(()"))

    def test_extract_variables_edge_cases(self):
        self.assertEqual(extract_variables("!a"), ['a'])
        self.assertEqual(extract_variables("a->a"), ['a'])
        self.assertEqual(extract_variables("(a)"), ['a'])
        self.assertEqual(extract_variables("a&b&c"), ['a', 'b', 'c'])

    def test_tokenize_edge_cases(self):
        self.assertEqual(tokenize("a"), ['a'])
        self.assertEqual(tokenize("!a"), ['!', 'a'])
        self.assertEqual(tokenize("a->b->c"), ['a', '->', 'b', '->', 'c'])
        self.assertEqual(tokenize(""), [])

    def test_shunting_yard_edge_cases(self):
        self.assertEqual(shunting_yard(['a']), ['a'])
        self.assertEqual(shunting_yard(['!', 'a']), ['a', '!'])
        self.assertEqual(shunting_yard(['a', '->', 'b', '->', 'c']),
                         ['a', 'b', '->', 'c', '->'])

    def test_evaluate_postfix_edge_cases(self):
        with self.assertRaises(ValueError):
            evaluate_postfix([], {'a': True})
        with self.assertRaises(ValueError):
            evaluate_postfix(['a', 'b', '^'], {'a': True, 'b': True})
        with self.assertRaises(ValueError):
            evaluate_postfix(['a', '&'], {'a': True})

    def test_generate_truth_table_edge_cases(self):
        with self.assertRaises(Exception):
            generate_truth_table([], ['a', 'b', '&'])
        with self.assertRaises(Exception):
            generate_truth_table(['a', 'b'], [])

    def test_print_truth_table(self):
        variables = ['a', 'b']
        table = [
            [False, False, False],
            [False, True, True],
            [True, False, False],
            [True, True, True]
        ]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_truth_table(variables, table)
            output = out.getvalue().strip()
            self.assertIn("a b | Result", output)
            self.assertIn("0 0 | 0", output)
            self.assertIn("DNF: (!a & b) | (a & b)", output)
        finally:
            sys.stdout = saved_stdout

    def test_main_invalid_input(self):
        with patch('builtins.input', return_value="a^b"):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                self.assertIn("Error: Invalid symbols in the formula.", fake_out.getvalue())

        with patch('builtins.input', return_value="(a"):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                self.assertIn("Error: Unbalanced parentheses.", fake_out.getvalue())


class TestMinimizer(unittest.TestCase):

    def test_get_binary(self):
        self.assertEqual(get_binary(0, 3), "000")
        self.assertEqual(get_binary(5, 4), "0101")
        self.assertEqual(get_binary(7, 3), "111")
        self.assertEqual(get_binary(15, 4), "1111")

    def test_count_ones(self):
        self.assertEqual(count_ones("000"), 0)
        self.assertEqual(count_ones("101"), 2)
        self.assertEqual(count_ones("1111"), 4)
        self.assertEqual(count_ones("1-0-"), 1)

    def test_can_combine(self):
        self.assertEqual(can_combine("000", "001"), (True, "00-"))
        self.assertEqual(can_combine("00-", "01-"), (True, "0--"))
        self.assertEqual(can_combine("000", "011"), (False, ""))

    def test_find_prime_implicants(self):
        primes, stages = find_prime_implicants([], 2)
        self.assertEqual(primes, [])
        self.assertEqual(stages, [])

        primes, stages = find_prime_implicants([0], 2)
        self.assertEqual(len(primes), 1)
        self.assertEqual(primes[0][0], "00")

        primes, stages = find_prime_implicants([0, 1, 2, 3], 2)
        self.assertEqual(len(primes), 2)
        self.assertEqual(primes[0][0], "--")

        primes, stages = find_prime_implicants([0, 1, 2, 5], 3)
        self.assertTrue(len(stages) > 0)

    def test_get_essential_primes(self):
        self.assertEqual(get_essential_primes([], set()), [])

        primes = [("00", {0})]
        essential = get_essential_primes(primes, {0})
        self.assertEqual(len(essential), 1)

        primes = [("00", {0}), ("01", {1}), ("--", {0, 1, 2, 3})]
        essential = get_essential_primes(primes, {0, 1, 2, 3})
        self.assertEqual(len(essential), 1)

        primes = [("00-", {0, 1}), ("0-1", {1, 3}), ("1-0", {4, 6})]
        essential = get_essential_primes(primes, {0, 1, 3, 4, 6})
        self.assertEqual(len(essential), 3)

    def test_pattern_to_expression(self):
        variables = ['a', 'b', 'c']

        self.assertEqual(pattern_to_expression("01-", variables, True), "!a & b")
        self.assertEqual(pattern_to_expression("1-0", variables, True), "a & !c")
        self.assertEqual(pattern_to_expression("--1", variables, True), "c")

        self.assertEqual(pattern_to_expression("01-", variables, False), "a | !b")
        self.assertEqual(pattern_to_expression("1-0", variables, False), "!a | c")
        self.assertEqual(pattern_to_expression("--1", variables, False), "!c")

    def test_get_karnaugh_map_size(self):
        self.assertEqual(get_karnaugh_map_size(2), (2, 2))
        self.assertEqual(get_karnaugh_map_size(3), (2, 4))
        self.assertEqual(get_karnaugh_map_size(4), (4, 4))
        self.assertEqual(get_karnaugh_map_size(5), (4, 8))

    def test_build_karnaugh_map(self):
        k_map = build_karnaugh_map([0, 3], 2)
        self.assertEqual(k_map, [[1, 0], [0, 1]])

        k_map = build_karnaugh_map([0, 1, 2, 5, 6, 7], 3)
        expected = [
            [1, 1, 0, 1],
            [0, 1, 1, 1]
        ]
        self.assertEqual(k_map, expected)

        k_map = build_karnaugh_map([], 2)
        self.assertEqual(k_map, [[0, 0], [0, 0]])

    def test_find_karnaugh_groups(self):
        self.assertEqual(find_karnaugh_groups([[0, 0], [0, 0]]), [])

        groups = find_karnaugh_groups([[1, 1], [1, 1]])
        self.assertEqual(len(groups), 1)

        k_map = [
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [1, 0, 0, 1]
        ]
        groups = find_karnaugh_groups(k_map)
        self.assertEqual(len(groups), 5)

    def test_karnaugh_group_to_expression(self):
        variables = ['a', 'b', 'c', 'd']
        k_map = build_karnaugh_map([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 4)

        group = (0, 0, 3, 3)
        expr = karnaugh_group_to_expression(group, k_map, variables, True)
        self.assertEqual(expr, "1")

        expr = karnaugh_group_to_expression(group, k_map, variables, False)
        self.assertEqual(expr, "0")

        k_map = build_karnaugh_map([0, 1, 4, 5], 3)
        group = (0, 0, 1, 1)
        expr = karnaugh_group_to_expression(group, k_map, variables[:3], True)
        self.assertEqual(expr, "!b")

    def test_minimize_sdnf(self):
        expr, stages = minimize_sdnf([], 2)
        self.assertEqual(expr, "Always False")

        expr, stages = minimize_sdnf([0], 2)
        self.assertEqual(expr, "(!a & !b)")

        expr, stages = minimize_sdnf([0, 1, 2, 3], 2)
        self.assertEqual(expr, "()")

        expr, stages = minimize_sdnf([0, 1, 2, 5], 3)
        self.assertTrue(len(stages) > 0)

    def test_minimize_sknf(self):
        expr, stages = minimize_sknf([], 2)
        self.assertEqual(expr, "Always True")

        expr, stages = minimize_sknf([0], 2)
        self.assertEqual(expr, "(a | b)")

        expr, stages = minimize_sknf([0, 1, 2, 3], 2)
        self.assertEqual(expr, "()")

        expr, stages = minimize_sknf([0, 1, 2, 5], 3)
        self.assertTrue(len(stages) > 0)

    def test_minimize_with_karnaugh_sdnf(self):
        expr, stages = minimize_with_karnaugh_sdnf([], 2)
        self.assertEqual(expr, "Always False")

        expr, stages = minimize_with_karnaugh_sdnf([0], 2)
        self.assertEqual(expr, "(!a & !b)")

        expr, stages = minimize_with_karnaugh_sdnf([0, 1, 2, 3], 2)
        self.assertEqual(expr, "1")

        expr, stages = minimize_with_karnaugh_sdnf([0, 1, 2, 5], 3)
        self.assertTrue(len(stages) > 0)

    def test_minimize_with_karnaugh_sknf(self):
        expr, stages = minimize_with_karnaugh_sknf([], 2)
        self.assertEqual(expr, "Always True")

        expr, stages = minimize_with_karnaugh_sknf([0], 2)
        self.assertEqual(expr, "(a | b)")

        expr, stages = minimize_with_karnaugh_sknf([0, 1, 2, 3], 2)
        self.assertEqual(expr, "0")

        expr, stages = minimize_with_karnaugh_sknf([0, 1, 2, 5], 3)
        self.assertTrue(len(stages) > 0)

    def test_calculate_coverage_table(self):
        primes = [("00", {0})]
        table, essential = calculate_coverage_table(primes, {0})
        self.assertEqual(len(table), 2)
        self.assertEqual(len(essential), 1)

        primes = [("00", {0}), ("01", {1}), ("11", {3})]
        table, essential = calculate_coverage_table(primes, {0, 1, 3})
        self.assertEqual(len(table), 4)
        self.assertEqual(len(essential), 3)

    def test_minimize_quine_mccluskey_sdnf(self):
        expr, stages = minimize_quine_mccluskey_sdnf([], 2)
        self.assertEqual(expr, "Always False")

        expr, stages = minimize_quine_mccluskey_sdnf([0], 2)
        self.assertEqual(expr, "(!a & !b)")

        expr, stages = minimize_quine_mccluskey_sdnf([0, 1, 2, 3], 2)
        self.assertEqual(expr, "Always True")

        expr, stages = minimize_quine_mccluskey_sdnf([0, 1, 2, 5], 3)
        self.assertTrue(len(stages) > 0)

    def test_minimize_quine_mccluskey_sknf(self):
        expr, stages = minimize_quine_mccluskey_sknf([], 2)
        self.assertEqual(expr, "Always True")

        expr, stages = minimize_quine_mccluskey_sknf([0], 2)
        self.assertEqual(expr, "(a | b)")

        expr, stages = minimize_quine_mccluskey_sknf([0, 1, 2, 3], 2)
        self.assertEqual(expr, "Always False")

        expr, stages = minimize_quine_mccluskey_sknf([0, 1, 2, 5], 3)
        self.assertTrue(len(stages) > 0)


if __name__ == '__main__':
    unittest.main()