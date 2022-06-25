def check_brackets(expr):
    brackets = []
    for token in expr:
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


def check_dots(expr):
    incorrect_decimal = []
    for token in expr:
        if token.replace('.', '').isdigit():
            count_dots = 0
            for char in token:
                if char == '.':
                    count_dots += 1
            if count_dots > 1:
                incorrect_decimal.append(token)
    if incorrect_decimal:
        raise ArithmeticError('Incorrect integer separators in numbers: %s' % ', '.join(incorrect_decimal))
