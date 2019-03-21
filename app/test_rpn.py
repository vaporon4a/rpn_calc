from contextlib import contextmanager
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest

from app.rpn import Rpn, InvalidOperationError


@contextmanager
def capture_stdout():
    tmp_out = StringIO()
    sys.stdout = tmp_out
    yield sys.stdout
    sys.stdout = sys.__stdout__

def test_push_simple():
    rpn = Rpn()
    assert rpn.stack == []
    rpn.push("12")
    assert rpn.stack == [12.0]
    rpn.push("12 3")
    assert rpn.stack == [12.0, 12.0, 3.0]
    rpn.push("-4")
    assert rpn.stack == [12.0, 12.0, 3.0, -4.0]
    rpn = Rpn()
    # Commas are interpreted as dots
    rpn.push("0 -1.3333 1,4444 0.0001")
    assert rpn.stack == [0, -1.3333, 1.4444, 0.0001]


def test_clear():
    rpn = Rpn()
    rpn.push("12 3 5 7 8")
    assert rpn.stack == [12.0, 3.0, 5.0, 7.0, 8.0]
    rpn.clear()
    assert rpn.stack == []


def test_push_error():
    rpn = Rpn()
    rpn.push('meuh')  # error
    assert rpn.stack == []


def test_drop():
    rpn = Rpn()
    with pytest.raises(InvalidOperationError):
        rpn.drop()  # Error
        assert rpn.stack == []
    rpn.push("1 2")
    rpn.drop()
    assert rpn.stack == [1.0]
    rpn.drop()
    assert rpn.stack == []


def test_get_status():
    rpn = Rpn()
    assert rpn.get_status() == "The stack is empty."
    rpn.push("1 2 3 4")
    assert rpn.get_status() == "4.0"


def test_plus():
    rpn = Rpn()
    rpn.push("+")  # Error
    assert rpn.stack == []
    rpn.push("12 3 +")
    assert rpn.stack == [15.0]
    rpn.push("+")  # Error
    assert rpn.stack == [15.0]

    # Chained operations
    rpn.clear()
    rpn.push("12 3 + 4 5 +")
    assert rpn.stack == [15.0, 9.0]


def test_minus():
    rpn = Rpn()
    rpn.push("-")  # Error
    assert rpn.stack == []
    rpn.push("12 3 -")
    assert rpn.stack == [9.0]
    rpn.push("-")  # Error
    assert rpn.stack == [9.0]

    # Chained operations
    rpn.clear()
    rpn.push("12 3 - 4 5 -")
    assert rpn.stack == [9.0, -1.0]


def test_multiply():
    rpn = Rpn()
    rpn.push("*")  # Error
    assert rpn.stack == []
    rpn.push("12 3 *")
    assert rpn.stack == [36.0]
    rpn.push("*")  # Error
    assert rpn.stack == [36.0]

    # Chained operations
    rpn.clear()
    rpn.push("12 3 * 4 5 *")
    assert rpn.stack == [36.0, 20.0]

    # Multiply by negative number
    rpn.clear()
    rpn.push("12 -3 *")
    assert rpn.stack == [-36.0]
    rpn.push("-2 *")
    assert rpn.stack == [72.0]


def test_divide():
    rpn = Rpn()
    rpn.push("/")  # Error
    assert rpn.stack == []
    rpn.push("12 3 /")
    assert rpn.stack == [4.0]
    rpn.push("/")  # Error
    assert rpn.stack == [4.0]

    # Chained operations
    rpn.clear()
    rpn.push("12 3 / 4 5 /")
    assert rpn.stack == [4.0, .8]

    # Divide by negative number
    rpn.clear()
    rpn.push("12 -3 /")
    assert rpn.stack == [-4.0]
    rpn.push("-2 /")
    assert rpn.stack == [2.0]

    # Division by zero
    rpn.clear()
    rpn.push("42 0 /")
    assert rpn.stack == [42.0, 0.]


def test_sin():
    rpn = Rpn()
    rpn.push('sin')  # error
    assert rpn.stack == []
    rpn.clear()
    rpn.push('90 sin')
    assert rpn.stack == [1.0]
    rpn.clear()
    rpn.push('0 sin')  # error
    assert rpn.stack == [0.0]
    
def test_cos():
    rpn = Rpn()
    rpn.push('cos') #error
    assert rpn.stack == []
    rpn.clear()
    rpn.push('360 cos')
    assert rpn.stack == [1.0]
    rpn.clear()
    rpn.push('0 cos')
    assert rpn.stack == [1.0]
    
