import logging
from sys import stdout

from calculator import calculate


logger = logging.getLogger('calculator')
logger.addHandler(logging.StreamHandler(stdout))


if __name__ == "__main__":
    while True:
        print('Choose in which form you plan to enter expressions: infix or postfix. Enter "exit" to terminate the program.')
        form = input()
        if form not in ['infix', 'postfix', 'exit']:
            print('Unknown command enter "infix", "postfix" or "exit"')
            continue
        if form == 'exit':
            exit()

        while True:
            print('\nEnter expression in %s form. '
                  'Enter "menu" to go to the selection of the form of the expression. '
                  'Enter "exit" to terminate the program.' % form)
            expr = input()
            if expr == 'exit':
                exit()
            elif expr == 'menu':
                break
            try:
                is_postfix = form=='postfix'
                result = calculate(expr, is_postfix=is_postfix)
                print(result)
            except (ArithmeticError, ValueError) as ex:
                logger.error(ex)
