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
