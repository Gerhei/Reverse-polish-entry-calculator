import logging
from sys import stdout

from calculator import calculate


logger = logging.getLogger('calculator')
logger.addHandler(logging.StreamHandler(stdout))


if __name__ == "__main__":
    history = []

    while True:
        print('Choose in which form you plan to enter expressions: infix or postfix. Enter "exit" to terminate the program.')
        form = input()
        if form not in ['infix', 'postfix', 'exit']:
            print('Unknown command enter "infix", "postfix" or "exit"')
            continue
        if form == 'exit':
            exit()

        while True:
            print('\nEnter expression in %s form.\n'
                  'Enter "menu" to go to the selection of the form of the expression.\n'
                  'Enter "exit" to terminate the program.\n'
                  'Enter "history" to see the entire history of calculations.' % form)
            expr = input()
            if expr == 'exit':
                exit()
            elif expr == 'menu':
                break
            elif expr == 'history':
                for elem in history:
                    print(elem)
                continue
            try:
                is_postfix = form=='postfix'
                result = calculate(expr, is_postfix=is_postfix)
                print(result)
                history.append(expr+' = '+str(result))
            except (ArithmeticError, ValueError) as ex:
                logger.error(ex)
