import unittest
from logic_engine import LogicalExpressionEvaluator

class TestLogicalExpressionEvaluator(unittest.TestCase):
    def test_tokenize(self):
        evaluator = LogicalExpressionEvaluator("a&!b")
        self.assertEqual(evaluator.tokens, ['a', '&', '!', 'b'])

    def test_rpn(self):
        evaluator = LogicalExpressionEvaluator("a & b | c")
        self.assertEqual(evaluator.rpn, ['a', 'b', '&', 'c', '|'])

    def test_eval_rpn(self):
        evaluator = LogicalExpressionEvaluator("a & !b")
        val = {'a': True, 'b': False}
        result = evaluator.eval_rpn(evaluator.rpn, val)
        self.assertTrue(result)

    def test_truth_table_len(self):
        evaluator = LogicalExpressionEvaluator("a | b")
        table = evaluator.generate_truth_table()
        self.assertEqual(len(table), 4)

    def test_sdnf(self):
        evaluator = LogicalExpressionEvaluator("a & b")
        table = evaluator.generate_truth_table()
        sdnf, idx = evaluator.build_sdnf(table)
        self.assertIn('(a & b)', sdnf)
        self.assertIn(3, idx)

    def test_sknf(self):
        evaluator = LogicalExpressionEvaluator("a & b")
        table = evaluator.generate_truth_table()
        sknf, idx = evaluator.build_sknf(table)
        self.assertIn('(a | b)', sknf)  # One of the minterms in SKNF
        self.assertIn(0, idx)

    def test_invalid_token(self):
        with self.assertRaises(ValueError):
            LogicalExpressionEvaluator("a # b")

    def test_equivalence(self):
        evaluator = LogicalExpressionEvaluator("a ~> a")
        table = evaluator.generate_truth_table()
        for _, result in table:
            self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
