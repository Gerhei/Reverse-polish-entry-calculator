import logging

from calculator import calculate


logger = logging.getLogger('calculator')
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    print('Enter expression in postfix form. Enter the exit to terminate the program.')
    while True:
        expr = input()
        if expr=='exit':
            break
        try:
            result = calculate(expr, is_postfix=True)
            print(result)
        except (ArithmeticError, ValueError) as ex:
            logger.error(ex)
