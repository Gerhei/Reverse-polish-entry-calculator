BINARY = ('+', '-', '*', '/', '^')
PRIORITY = {"^": 3, "/": 2, "*": 2, "-": 1, "+": 1}


def parse_expression(expr):
    """
    Parses the expression to further calculation and removes spaces, extra dots in decimal numbers, etc.
    :param expr: string with a mathematical expression in infix or postfix form
    :return: list of expression tokens or raise error if the expression contains critical errors.
    """
    list_tokens = []
    token = ''
    count_point = 0
    for char in expr:
        if char.isdigit():
            token += char
            continue
        elif char == '.':
            if count_point<1:
                token += char
            count_point += 1
            continue
        if token: list_tokens.append(token)
        count_point = 0
        token = ''

        if char in BINARY or char in ['(', ')']:
            list_tokens.append(char)
        elif char == ' ':
            continue
        else:
            raise ArithmeticError('Find unknown operation or value: %s' % char)
    if token: list_tokens.append(token)

    return list_tokens


def convert_to_postfix_form(expr):
    """
    :param expr: string with a mathematical expression in infix form
    :return: expression postfix form in list format
    """
    postfix_form = []
    stack = []
    list_tokens = parse_expression(expr)

    for token in list_tokens:
        if token.replace('.', '', 1).isdigit():
            postfix_form.append(token)

        if token in BINARY:
            while stack and (stack[-1] not in ['(', ')']) and (PRIORITY[token]<=PRIORITY[stack[-1]]):
                postfix_form.append(stack[-1])
                stack.pop()
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1]!='(':
                postfix_form.append(stack[-1])
                stack.pop()
            if not stack:
                raise ArithmeticError('"(" is missing.')
            stack.pop()

    while stack:
        if stack[-1] == "(":
           raise ArithmeticError('")" is missing.')
        postfix_form.append(stack[-1])
        stack.pop()

    return postfix_form


def calculate(expr, is_postfix=True):
    """
    :param expr: string with a mathematical expression in infix or postfix form
    :param is_postfix: if the expression is in postfix form this parameter must be True
    :return: the result of executing a mathematical expression
    """
    stack = []
    if not is_postfix:
        expr = convert_to_postfix_form(expr)
    else:
        expr = parse_expression(expr)
    expr.reverse()

    while expr:
        token = expr.pop()
        if token.replace('.', '', 1).isdigit():
            stack.append(token)
        if token in BINARY:
            try:
                right_oper = float(stack.pop())
                if stack:
                    left_oper = float(stack.pop())
                elif token=='-':
                    left_oper = 0
                else:
                    raise ArithmeticError
            except (IndexError, ArithmeticError):
                raise ArithmeticError('For operation "%s" missing operands' % token)
            stack.append(calculate_binary_expression(left_oper, right_oper, token))

    if not stack:
        raise ValueError('There is no expression to calculate.')
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
