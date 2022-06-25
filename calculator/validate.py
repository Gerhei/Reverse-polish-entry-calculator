from operations import UNARY, BINARY, BRACKETS


def check_brackets(list_tokens):
    brackets = []
    for token in list_tokens:
        if token == '(':
            brackets.append(token)
        elif token == ')':
            try:
                index = brackets.index('(')
                brackets.pop(index)
            except ValueError:
                brackets.append(token)
                break
    if brackets:
        raise ArithmeticError('Unclosed bracket: "%s"' % brackets[-1])


def check_dots(list_tokens):
    incorrect_decimal = []
    for token in list_tokens:
        if token.replace('.', '').isdigit():
            count_dots = 0
            for char in token:
                if char == '.':
                    count_dots += 1
            if count_dots > 1:
                incorrect_decimal.append(token)
    if incorrect_decimal:
        raise ArithmeticError('Incorrect integer separators in numbers: %s' % ', '.join(incorrect_decimal))


def check_unknown_operation(list_tokens):
    for token in list_tokens:
        if not token.replace('.', '', 1).isdigit():
            if token.isalpha():
                if len(token) > 1 and (token not in UNARY+BINARY):
                    # it is not a variable, but unknown operation
                    raise ArithmeticError('Unknown operations: %s' % token)
            elif token not in UNARY+BINARY+BRACKETS:
                raise ArithmeticError('Unknown operations: %s' % token)
