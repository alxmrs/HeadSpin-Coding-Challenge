## 1) Later: Parallel-asynchronous framework.


Implement a tiny asynchronous programming framework, supporting
_asynchronous_ function calls and _synchronous_ callbacks.


Asynchronous function call:

An asynchronous function call, unlike a normal call, does not wait for
the function to complete before returning. It calls the function and
returns immediately. The result of the function will have to be
handled differently than a normal function call.


Implement a function called "async" that can be called as:
```
   async(fn, arg1, arg2, ...)(callback)
```
"fn" is a normal function and "arg1", "arg2", etc., are the arguments
to this function. A normal call to "fn", for example
```
   fn(1, 2)
```
will run in line -- you have to wait for it to finish before calling
another function on that thread. An async call, for example,
```
   async(fn, 1, 2)(callback)
```
will return instantly, and return nothing. It will have invoked
"fn(1,2)" in a separate execution context. Later, when fn(1, 2)
finishes, the function "callback" is invoked with the return value of
"fn(1,2)".

"callback" takes two arguments. The first argument is the return value
of "fn(arg1, arg2, ...)" and the second argument is an exception
object, if an exception was thrown while running "fn(arg1, arg2, ...)".

In other words, the signature of "callback" is "callback(value, error)".
If "error" is null, then "value" is the return value of "fn". Otherwise, the
call failed and "error" contains the exception.


Important properties:


1. Async function calls should run in parallel with each other. For example,
```
  async(fib, 30)(handle_fib)
  async(multiply, 5, 57)(handle_multiply)
```
"multiply" should start running before "fib" returns. This means you
cannot use an approach where the async functions are queued up and
processed serially.


2. Callbacks should run in series with each other.

In contrast with async functions, all the callbacks from all the "async"
calls _are_ run synchronously -- one after the other. I.e. no two callbacks
are ever run in parallel with each other.


Deliverable:

Implement a Python module called "later". It should provide the
function "later.async()" described above. It may provide other
functions as well, if needed. For example, a "start()" or "init()"
function that does any necessary setup.

Here's a possible usage:
```
import later

def mul(x, y):
    return x * y

def fib(x):
    if x < 2:
        return x
    else:
        return fib(x-1) + fib(x-2)

def print_result(value, error):
    if error is not None:
        print 'There was an error.'
    else:
        print value

if __name__ == "__main__":
    later.start()
    later.async(fib, 30)(print_result)
    later.async(mul, 50, 60)(print_result)
```
A program using "later" should exit normally when all functions and
callbacks have completed execution. If the main thread reaches the end
of the program, the program needs to wait for all asynchronous
functions and their callbacks to finish processing. Once all functions and
callbacks have finished, the program exits instantly.

The program also exits instantly when the user hits Ctrl-C, without waiting
for any async functions or callbacks to finish.

