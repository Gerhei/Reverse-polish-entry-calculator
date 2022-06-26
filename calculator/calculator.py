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

    previous = None
    for token in expr:
        # if number or variable
        if token.replace('.', '', 1).isdigit() or (len(token) == 1 and token.isalpha()):
            postfix_form.append(token)

        if token in BINARY+UNARY:
            if token == '-':
                if not previous or previous in BINARY + UNARY + ('(',):
                    # unary minus
                    token = '~'
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
        previous = token

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
    stack_with_variables = []
    expr = parse_expression(expr)
    check_brackets(expr)
    check_dots(expr)
    check_unknown_operation(expr)

    if not is_postfix:
        expr = convert_to_postfix_form(expr)

    while expr:
        token = expr.pop(0)
        # if number or variable
        if token.replace('.', '', 1).isdigit() or (len(token) == 1 and token.isalpha()):
            stack.insert(0, token)

        # if the expression is enter in a postfix form,
        # then the check for a unary minus has not yet been performed
        if is_postfix and token == '-':
            if len(stack) == 1:
                token = '~'

        try:
            if token in BINARY:
                right_oper = stack.pop(0)
                left_oper = stack.pop(0)
                numbers, variables = split_operands(str(left_oper), str(right_oper))
                if len(numbers) == 2:
                    # operation with numbers
                    stack.insert(0, calculate_binary_expression(left_oper, right_oper, token))
                elif len(variables) == 2 or len(variables) == 1 and not numbers:
                    # operation with variables
                    stack_with_variables.extend([*variables, token])
                else:
                    # operation with number and variables
                    stack_with_variables.extend([*variables, token])
                    stack.insert(-1, *numbers)

            elif token in UNARY:
                oper = stack.pop(0)
                if str(oper).isalpha():
                    stack_with_variables.extend([oper, token])
                else:
                    stack.insert(0, calculate_unary_expression(oper, token))
        except IndexError:
            if stack_with_variables:
                stack_with_variables.extend([right_oper, token])
                break
            else:
                raise ArithmeticError('For operation "%s" missing operand' % token)

    result = []
    if stack_with_variables:
        for elem in stack+stack_with_variables:
            result.append(str(elem))
        result = " ".join(result)
    else:
        result = stack[0]
    if not result:
        raise ValueError('There is no expression to calculate.')
    elif len(stack) > 1:
        raise ArithmeticError('There are extra operands.')

    return result


def calculate_binary_expression(left_oper, right_oper, operation):
    left_oper = float(left_oper)
    right_oper = float(right_oper)

    if operation=="+":
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


def calculate_unary_expression(operand, operation):
    operand = float(operand)
    if operation=="~":
        result = -operand
    return result


def split_operands(left_oper, right_oper):
    """Divides the expression into 2 parts: numbers and variables"""
    numbers = []
    variables = []
    if left_oper.isalpha():
        variables.append(left_oper)
    else:
        numbers.append(left_oper)

    if right_oper.isalpha():
        variables.append(right_oper)
    else:
        numbers.append(right_oper)

    return numbers, variables
