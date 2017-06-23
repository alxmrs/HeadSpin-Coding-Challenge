
# HeadSpin Coding Challenge

## Challenge Description

There are two problem for this coding challenge.
Each are defined inside their module directory. 

1. [Later](/later/README.md)
2. [HTTP and Sockets](/http_and_sockets/README.md)

## Requirements

Python 3.X (written in 3.6)


## How to use

1. Later

Later lets you run a function _asynchronously_ with a _synchronous_ callback.  
Use it like so:  

```python
import later


def fib(x):
    if x < 2:
        return x
    else:
        return fib(x - 1) + fib(x - 2)
        
def print_result(val, error):
    if error is not None:
        print('An error occurred')
    else:
        print(val)
        
later.async(fib, 10)(print_result)

```

Unit tests for this module can be found in the `tests` directory. 

2. HTTP and Sockets

This solution can be demonstrated with the following: 

```python
from http_and_sockets import GET, process_response

resp = GET('http://www.google.com/search?q=HeadSpin')
process_response(resp)
```

Run `python ./http_and_sockets/my_request.py` to see this in action.
