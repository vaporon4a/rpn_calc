#!venv/bin/python
# -*- coding: utf-8 -*-

import math
from collections import _chain




class InvalidOperationError(Exception):
    def __init__(self, message):
        super(InvalidOperationError, self).__init__(message)
        self.digits = []


class OneDigitError(InvalidOperationError):

    def __init__(self, message, digit=None):
        super(OneDigitError, self).__init__(message)
        self.digits = [digit]


class TwoDigitError(InvalidOperationError):

    def __init__(self, message, digit1=None, digit2=None):
        super(TwoDigitError, self).__init__(message)
        self.digits = [digit2, digit1]


def to_float(item):
    return float(item.replace(',', '.'))


def is_numeric(item):
    try:
        to_float(item)
        return True
    except (ValueError, TypeError):
        pass
    return False


class Rpn(object):
    def __init__(self):
        self.stack = []
        self.errors = []
        self.ONE_ITEM_OPS = {
            'sin': self.sin,
            'cos': self.cos,
        }
        self.TWO_ITEM_OPS = {
            '+': self.plus,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,
        }
        self.ALL_OPS = list(_chain(
            self.TWO_ITEM_OPS.keys(),
            self.ONE_ITEM_OPS.keys(),
        ))


    def handle_op(self, operator):
        # If not in the operators, abort
        if operator not in self.ALL_OPS:
            self.errors.append("Error: `{}` unknown".format(operator))
            raise InvalidOperationError("Error: `{}` unknown".format(operator))

        if operator in self.ONE_ITEM_OPS:
            if len(self.stack) < 1:
                self.errors.append("{}: Invalid stack length".format(operator))
                raise InvalidOperationError(
                    "{}: Invalid stack length".format(operator))
            digit = self.stack.pop()
            f = self.ONE_ITEM_OPS[operator]
            return f(digit)
        elif operator in self.TWO_ITEM_OPS:
            if len(self.stack) < 2:
                self.errors.append("{}: Invalid stack length".format(operator))
                raise InvalidOperationError(
                    "{}: Invalid stack length".format(operator))
            digit1, digit2 = self.stack.pop(), self.stack.pop()
            f = self.TWO_ITEM_OPS[operator]
            return f(digit1, digit2)

    # -- Stack operations
    def push(self, input_buffer):

        result = []
        items = input_buffer.split()
        for item in items:
            try:
                if is_numeric(item):
                    self.stack.append(to_float(item))
                else:
                    result = self.handle_op(item)
            except InvalidOperationError as msg:
                print(msg)
                # catch digits back
                if msg.digits:
                    self.stack.extend(msg.digits)

            while result:
                self.stack.append(result.pop())

        print('stack: {}'.format(self.stack))

    def clear(self):
        self.stack = []
        self.errors = []

    def get_status(self):
        if self.stack:
            return str(self.stack[-1])
        return "The stack is empty."

    # -- Math operators
    def plus(self, digit1, digit2):
        return [digit1 + digit2]

    def minus(self, digit1, digit2):
        return [digit2 - digit1]

    def multiply(self, digit1, digit2):
        return [digit1 * digit2]

    def divide(self, digit1, digit2):
        try:
            return [digit2 / digit1]
        except ZeroDivisionError:
            raise TwoDigitError(
                "divide: Division by Zero", digit1=digit1, digit2=digit2)

    def sin(self, digit):
        return [math.sin(math.radians(digit))]
        
    def cos(self, digit):
        return [math.cos(math.radians(digit))]
        
