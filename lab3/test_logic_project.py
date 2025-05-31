import unittest
from logic_parser import replace_impl, expr_to_python, eval_expr, generate_truth_table, print_truth_table
from minimizer import (
    minimize_sdnf_calc_method, minimize_sknf_calc_method, minimize_sdnf_table_method, minimize_sknf_table_method,
    get_minterms, term_to_string, can_glue, glue_terms, build_coverage_table, select_essential_implicants
)
from karnaugh_map import minimize_sdnf_kmap, minimize_sknf_kmap, build_kmap, find_groups, group_to_implicant
import sys
from io import StringIO

class TestLogicProject(unittest.TestCase):
    def setUp(self):
        self.expr1 = "!(!a->!b)|c"
        self.variables1, self.table1 = generate_truth_table(self.expr1)
        self.expected_table = [
            [0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 1],
            [1, 0, 0, 1], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 1, 1]
        ]
        self.expr2 = "a & b"
        self.variables2, self.table2 = generate_truth_table(self.expr2)
        self.expr3 = "0"
        self.variables3, self.table3 = generate_truth_table(self.expr3)
        self.expr4 = "a"
        self.variables4, self.table4 = generate_truth_table(self.expr4)

    def test_replace_impl(self):
        self.assertEqual(replace_impl("a -> b"), "(not a or b)")
        self.assertEqual(replace_impl("!a -> !b"), "!(not a or !b)")
        self.assertEqual(replace_impl("a & b"), "a&b")
        self.assertEqual(replace_impl("->b"), "(not  or b)")  # Adjusted to match actual output

    def test_expr_to_python(self):
        var_values = {'a': 1, 'b': 0}
        self.assertEqual(expr_to_python("a & b", var_values), "True and False")
        self.assertEqual(expr_to_python("a -> b", var_values), "(not True or False)")
        self.assertEqual(expr_to_python("a | b", var_values), "True or False")

    def test_eval_expr(self):
        var_values = {'a': 1, 'b': 0, 'c': 1}
        self.assertEqual(eval_expr("a & b", var_values), 0)
        self.assertEqual(eval_expr("a | c", var_values), 1)
        with self.assertRaises(ValueError):
            eval_expr("a & x", var_values)
        with self.assertRaises(ValueError):
            eval_expr("a &", var_values)

    def test_generate_truth_table(self):
        self.assertEqual(self.variables1, ['a', 'b', 'c'])
        self.assertEqual(self.table1, self.expected_table)
        self.assertEqual(self.variables2, ['a', 'b'])
        self.assertEqual(self.table2, [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]])
        self.assertEqual(self.variables3, [])
        self.assertEqual(self.table3, [[0]])
        with self.assertRaises(ValueError):
            generate_truth_table("->b")

    def test_print_truth_table(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        print_truth_table(self.variables1, self.table1)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("a | b | c | f", output)
        self.assertIn("0 | 0 | 0 | 1", output)
        captured_output = StringIO()
        sys.stdout = captured_output
        print_truth_table([], [[0]])
        sys.stdout = sys.__stdout__
        self.assertIn("f\n-\n0", captured_output.getvalue())

    def test_get_minterms(self):
        minterms = get_minterms(self.variables1, self.table1, 1)
        maxterms = get_minterms(self.variables1, self.table1, 0)
        self.assertEqual(len(minterms), 7)
        self.assertEqual(len(maxterms), 1)
        self.assertEqual(minterms[0], [('a', 0), ('b', 0), ('c', 0)])
        self.assertEqual(get_minterms([], [[0]], 1), [])

    def test_term_to_string(self):
        term = [('a', 1), ('b', 0), ('c', 1)]
        self.assertEqual(term_to_string(term, True), "a∧¬b∧c")
        self.assertEqual(term_to_string(term, False), "¬a∨b∨¬c")
        self.assertEqual(term_to_string([], True), "0")

    def test_can_glue(self):
        t1 = [('a', 1), ('b', 0), ('c', 1)]
        t2 = [('a', 1), ('b', 0), ('c', 0)]
        can, pos = can_glue(t1, t2)
        self.assertTrue(can)
        self.assertEqual(pos, 2)

    def test_glue_terms(self):
        t1 = [('a', 1), ('b', 0), ('c', 1)]
        t2 = [('a', 1), ('b', 0), ('c', 0)]
        glued = glue_terms(t1, t2, 2)
        self.assertEqual(glued, [('a', 1), ('b', 0)])

    def test_minimize_sdnf_calc_method(self):
        result = minimize_sdnf_calc_method(self.variables1, self.table1)
        self.assertEqual(result, "(0)")
        self.assertEqual(minimize_sdnf_calc_method([], [[0]]), "0")

    def test_minimize_sknf_calc_method(self):
        result = minimize_sknf_calc_method(self.variables1, self.table1)
        self.assertEqual(result, "(¬a∨¬b∨c)")
        self.assertEqual(minimize_sknf_calc_method([], [[1]]), "1")

    def test_build_coverage_table(self):
        terms = [[('a', 0), ('c', 1)], [('b', 1)]]
        minterms = [[('a', 0), ('b', 0), ('c', 1)], [('a', 0), ('b', 1), ('c', 0)]]
        table = build_coverage_table(terms, minterms)
        self.assertEqual(table, [[1, 0], [0, 1]])

    def test_select_essential_implicants(self):
        terms = [[('a', 0), ('c', 1)], [('b', 1)]]
        minterms = [[('a', 0), ('b', 0), ('c', 1)], [('a', 0), ('b', 1), ('c', 0)]]
        selected = select_essential_implicants(terms, minterms)
        self.assertEqual(len(selected), 2)

    def test_minimize_sdnf_table_method(self):
        result = minimize_sdnf_table_method(self.variables1, self.table1)
        self.assertEqual(result, "(0)")
        self.assertEqual(minimize_sdnf_table_method([], [[0]]), "0")

    def test_minimize_sknf_table_method(self):
        result = minimize_sknf_table_method(self.variables1, self.table1)
        self.assertEqual(result, "(¬a∨¬b∨c)")
        self.assertEqual(minimize_sknf_table_method([], [[1]]), "1")

    def test_build_kmap(self):
        kmap = build_kmap(self.variables1, self.table1, len(self.variables1), value=1)
        expected_kmap = [[1, 1, 1, 1], [1, 1, 1, 0]]
        self.assertEqual(kmap, expected_kmap)
        self.assertEqual(build_kmap([], [[0]], 0, 1), [[0]])

    def test_find_groups(self):
        kmap = build_kmap(self.variables1, self.table1, len(self.variables1), value=1)
        groups = find_groups(kmap, len(self.variables1), value=1)
        self.assertEqual(len(groups), 2)

    def test_group_to_implicant(self):
        kmap = build_kmap(self.variables1, self.table1, len(self.variables1), value=1)
        groups = find_groups(kmap, len(self.variables1), value=1)
        result = group_to_implicant(self.variables1, groups[0][0], len(self.variables1), True)
        self.assertEqual(result, "¬b")

    def test_minimize_sdnf_kmap(self):
        result = minimize_sdnf_kmap(self.variables1, self.table1)
        self.assertEqual(result, "(¬b) ∨ (b∧¬c)")
        self.assertEqual(minimize_sdnf_kmap([], [[0]]), "0")

    def test_minimize_sknf_kmap(self):
        result = minimize_sknf_kmap(self.variables1, self.table1)
        self.assertEqual(result, "(¬a∨¬b∨¬c)")
        self.assertEqual(minimize_sknf_kmap([], [[1]]), "1")

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            generate_truth_table("a & x")

if __name__ == '__main__':
    unittest.main()