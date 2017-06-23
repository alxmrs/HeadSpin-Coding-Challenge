import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor


_pool = None


def start():
    """Initializes the process pool for the async method."""
    global _pool
    if _pool is None:
        _pool = ProcessPoolExecutor(mp.cpu_count()+2)


def async(fn, *args):
    """
    Will execute the input function asynchronously with its input args.
    Returns a function (wrapper) that takes a callback. The wrapper function will
    call the callback with the result of the input function (fn) or an error if one should arise.

    :param fn: A function which takes zero or more arguments
    :param args: arguments for fn
    :return: a function that takes a callback (the callback takes (value, error) as inputs)
    """

    global _pool

    if _pool is None:
        start()

    future = _pool.submit(fn, *args)

    def wrapper(callback):

        def future_cb(f):
            err = f.exception()
            if err:
                callback(None, err)
            else:
                callback(f.result(), None)

        future.add_done_callback(future_cb)

    return wrapper


