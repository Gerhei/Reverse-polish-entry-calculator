from validate import *
from operations import *


def parse_expression(expr):
    """
    Parses the expression to further calculation and removes spaces, extra dots in decimal numbers, etc.
    :param expr: string with a mathematical expression in infix or postfix form
    :return: list of expression tokens or raise error if the expression contains critical errors.
    """
    list_tokens = []
    token = ''
    for char in expr:
        if char.isdigit() or char == '.':
            # parse number
            token += char
            continue
        elif char.isalpha():
            # parse variable or operations (sin, cos for example)
            token += char
            continue
        if token:
            list_tokens.append(token)
        token = ''

        if char == ' ':
            continue
        else:
            # parse other ('+', '-', '@', etc.)
            list_tokens.append(char)
    if token:
        list_tokens.append(token)
    return list_tokens


def convert_to_postfix_form(expr):
    """
    :param expr: string with a mathematical expression in infix form
    :return: expression postfix form in list format
    """
    postfix_form = []
    stack = []

    for token in expr:
        if token.replace('.', '', 1).isdigit():
            postfix_form.append(token)

        if token in BINARY:
            while stack and (stack[-1] not in ['(', ')']) and (PRIORITY[token]<=PRIORITY[stack[-1]]):
                postfix_form.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1]!='(':
                postfix_form.append(stack.pop())
            if stack:
                stack.pop()

    while stack:
        postfix_form.append(stack.pop())

    return postfix_form


def calculate(expr, is_postfix=True):
    """
    :param expr: string with a mathematical expression in infix or postfix form
    :param is_postfix: if the expression is in postfix form this parameter must be True
    :return: the result of executing a mathematical expression
    """
    stack = []
    expr = parse_expression(expr)
    check_brackets(expr)
    check_dots(expr)
    check_unknown_operation(expr)

    if not is_postfix:
        expr = convert_to_postfix_form(expr)

    while expr:
        token = expr.pop(0)
        if token.replace('.', '', 1).isdigit():
            stack.insert(0, token)
        if token in BINARY:
            try:
                right_oper = float(stack.pop(0))
                if stack:
                    left_oper = float(stack.pop(0))
                elif token=='-':
                    left_oper = 0
                else:
                    raise ArithmeticError
            except (IndexError, ArithmeticError):
                raise ArithmeticError('For operation "%s" missing operands' % token)
            stack.insert(0, calculate_binary_expression(left_oper, right_oper, token))

    if not stack:
        raise ValueError('There is no expression to calculate.')
    elif len(stack) > 1:
        raise ArithmeticError('There are extra operands.')
    return stack[0]


def calculate_binary_expression(left_oper, right_oper, operation):
    if operation=='+':
        result = left_oper + right_oper
    elif operation=="-":
        result = left_oper - right_oper
    elif operation=="*":
        result = left_oper * right_oper
    elif operation=="/":
        if right_oper==0:
            raise ZeroDivisionError('Dividing "%s" by zero' % left_oper)
        result = left_oper / right_oper
    elif operation=="^":
        result = left_oper ** right_oper
    return result
