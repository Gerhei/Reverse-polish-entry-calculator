import unittest
from unittest import skip

from calculator import *


class CalculatorTestCase(unittest.TestCase):
    def test_incorrect_float_number(self):
        incorrect_float_numbers = ['1.2.3', '1..2', '..4..', '.3.4', '.57.']
        for num in incorrect_float_numbers:
            with self.assertRaises(ArithmeticError):
                calculate(num, is_postfix=False)

    def test_correct_infix_expressions(self):
        corr_expr = {'1+2': 3, '2*(3+4)': 14, '-2+1': -1, '1.2*4': 4.8, '01.4-5': -3.6, '.43+5': 5.43,
                     '-.5+1': 0.5, '2/4^2': 0.125, '(3+2)*(4-1)': 15, '-4': -4, '-(4+5)': -9, '4.+1': 5,
                     '2*(-4+1)': -6.0, '2^(1+3)': 16}
        for expr, result in corr_expr.items():
            self.assertEqual(result, calculate(expr, is_postfix=False))

    def test_correct_postfix_expression(self):
        corr_expr = {'2 2 +': 4, '2 3 + 5 6 + *': 55, '5 - 1 +': -4, '0.5 2 *': 1.0, '01.4 5 -': -3.6,
                     '3 3 / 2 *': 2, '4 - 1 + 2 *': -6, '4 5 + -': -9, '4 -': -4, '2 - 4 +': 2}
        for expr, result in corr_expr.items():
            self.assertEqual(result, calculate(expr, is_postfix=True))

    def test_incorrect_infix_brackets(self):
        expr_with_brackets = ['((4+5)', ')-4*(7+8)', ')(', '(5-7)/(3*6', '(((1+2', '(5*6))']
        for expr in expr_with_brackets:
            with self.assertRaises(ArithmeticError):
                calculate(expr, is_postfix=False)

    def test_unknown_infix_operations(self):
        expr_with_unknown_operations = ['5[3', 'test', '0+1?', '2+@']
        for expr in expr_with_unknown_operations:
            with self.assertRaises(ArithmeticError):
                calculate(expr, is_postfix=False)

    def test_unknown_postfix_operations(self):
        expr_with_unknown_operations = ['45 ] [', 'test', '2 @ +']
        for expr in expr_with_unknown_operations:
            with self.assertRaises(ArithmeticError):
                calculate(expr, is_postfix=True)

    def test_incorrect_infix_operations(self):
        expr_with_incorrect_operations = ['**5', '-*4-', '2*-*9.7', '2++2']
        for expr in expr_with_incorrect_operations:
            with self.assertRaises(ArithmeticError):
                calculate(expr, is_postfix=False)

    def test_incorrect_postfix_operations(self):
        expr_with_incorrect_operations = ['5 + +', '4 + - *', '2 4 + - *', '+ - 6', '- 6 +', '+ -']
        for expr in expr_with_incorrect_operations:
            with self.assertRaises(ArithmeticError):
                calculate(expr, is_postfix=True)

    def test_extra_infix_operand(self):
        expr_with_extra_operands = ['2+2 2', '(5 3 + 1) * 2', '2 2', '6+4*(3 3)', '-6 6']
        for expr in expr_with_extra_operands:
            with self.assertRaises(ArithmeticError):
                calculate(expr, is_postfix=False)

    def test_extra_postfix_operands(self):
        expr_with_extra_operands = ['3 4 5 6 +', '2 2 + 2', '3 3', '7 5 6 +']
        for expr in expr_with_extra_operands:
            with self.assertRaises(ArithmeticError):
                calculate(expr, is_postfix=True)

    @skip
    def test_infix_expression_with_variables(self):
        expr_with_variables = {'2+a': '2+a', 'a+b': 'a+b', '2+4+a': '6+a', '2+a+b+3': '5+a+b'}
        for expr, result in expr_with_variables.items():
            self.assertEqual(result, calculate(expr, is_postfix=False))

    def test_postfix_expression_with_variables(self):
        expr_with_variables = {'4 a +': '4 a +', '5 4 + a *': '9.0 a *', '2 a + b + 3 +': '5.0 a + b +',
                               '2 3 + a + b +': '5.0 a + b +', '2 a + 3 +': '5.0 a +', 'a 2 +': '2 a +',
                               'a 2 + 3 + b +': '5.0 a + b +', 'a 2 + 3 +': '5.0 a +',
                               'a b + 3 +': 'a b + 3 +', '2 a * 3 +': '2 a * 3 +', '2 a * 3 *': '6.0 a *',
                               '2 a b * + 3 +': 'a b * 5 +'}
        for expr, result in expr_with_variables.items():
            self.assertEqual(result, calculate(expr, is_postfix=True))


if __name__ == '__main__':
    unittest.main()
