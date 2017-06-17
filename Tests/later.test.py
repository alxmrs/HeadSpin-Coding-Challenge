import unittest
from Later.later import start, async

from contextlib import contextmanager
from io import StringIO
import sys
import time

_fail_text = 'There was an error.'


class AsyncTests(unittest.TestCase):
    def test_general(self):
        start()

        with captured_output() as (out, err):
            async(fib, 30)(print_result)
            time.sleep(2)

        output = out.getvalue()

        self.assertEqual(int(output), 832040)

    def test_bad_function(self):
        start()

        with captured_output() as (out, err):
            async(fib_fail, 10)(print_result)
            time.sleep(1)

        output = out.getvalue()

        self.assertEqual(output, _fail_text + '\n')

    def test_asynchronous_property(self):
        start()

        finish_last = "called first, finished last"
        finish_first = "called second, finish first"

        expected = '\n'.join([finish_first, finish_last]) + '\n'

        with captured_output() as (out, err):
            async(wait_and_return, 5, finish_last)(print_result)
            async(wait_and_return, .5, finish_first)(print_result)
            time.sleep(6)
        output = out.getvalue()

        self.assertEqual(output, expected)

    def test_mult_vs_fib(self):

        expected = '100\n832040\n'

        with captured_output() as (out, err):
            async(fib, 30)(print_result)
            async(multiply, 10, 10)(print_result)
            time.sleep(1)
        output = out.getvalue()

        self.assertEqual(output, expected)


def fib(x):
    if x < 2:
        return x
    else:
        return fib(x - 1) + fib(x - 2)


def multiply(x, y):
    return x * y


def fib_fail(x):
    if x < 2:
        return x
    else:
        return fib_fail(x-1) + fail(x-2)


def print_result(val, error):
    if error is not None:
        print(_fail_text)
    else:
        print(val)


def wait_and_return(t, retval):
    import time

    time.sleep(t)

    return retval


def return_result(val, error):
    if error is not None:
        return _fail_text
    else:
        return val

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

if __name__ == '__main__':
    unittest.main()
