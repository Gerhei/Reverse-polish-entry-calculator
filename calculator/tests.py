import unittest

from calculator import *


class CalculatorTestCase(unittest.TestCase):
    allowed_error = 0.001

    def test_correct_expressions(self):
        corr_expr = {'1+2': 3, '2*(3+4)': 14, '-2+1': -1, '1.2*4': 4.8, '01.4-5': -3.6, '.43+5': 5.43,
                     '-.67+1': 0.33, '2/4^2': 0.125, '(3+2)*(4-1)': 15, '-4': -4, '-(4+5)': -9}
        for expr, result in corr_expr.items():
            is_equal = abs(result - calculate(expr, False)) <= self.allowed_error
            self.assertTrue(is_equal)

    def test_writing_float_number(self):
        float_numbers = {'1.2.3': '1.23', '1..2.': '1.2', '..4..': '.4', '.3.4': '.34'}
        for string, num in float_numbers.items():
            self.assertEqual(num, parse_expression(string)[0])

    def test_incorrect_brackets(self):
        expr_with_brackets = ['((4+5)', ')-4*(7+8)', ')(', '(5-7)/(3*6']
        for expr in expr_with_brackets:
            with self.assertRaises(ArithmeticError):
                calculate(expr, False)

    def test_unknown_operations(self):
        expr_with_unknown_operations = ['4+a', '5[3', 'test', '0+1?']
        for expr in expr_with_unknown_operations:
            with self.assertRaises(ArithmeticError):
                calculate(expr, False)

    def test_incorrect_operations(self):
        expr_with_incorrect_operations = ['**5', '-*4-', '2*-*9.7', '2++2']
        for expr in expr_with_incorrect_operations:
            with self.assertRaises(ArithmeticError):
                calculate(expr, False)

if __name__ == '__main__':
    unittest.main()
