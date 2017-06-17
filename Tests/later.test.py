import unittest
from Later.later import start, async

from contextlib import contextmanager
from io import StringIO
import sys

_fail_text = 'There was an error.'


class AsyncTests(unittest.TestCase):
    # def test_general(self):
    #     start()
    #
    #     async(fib, 30)(print_result)
    #
    #     result = async(fib, 30)(return_result)
    #
    #     self.assertEqual(result, 832040)
    #
    # def test_bad_function(self):
    #     start()
    #
    #     result = async(fib_fail, 10)(return_result)
    #
    #     self.assertEqual(result, _fail_text)

    def test_asynchronous_property(self):
        start()

        expected = "called second, finish first\ncalled first, finished last\n"

        with captured_output() as (out, err):
            async(wait_and_return, 2, "called first, finished last")(print_result)
            async(wait_and_return, 1, "called second, finish first")(print_result)

        output = out.getvalue()

        self.assertEqual(output, expected)




def fib(x):
    if x < 2:
        return x
    else:
        return fib(x - 1) + fib(x - 2)


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
