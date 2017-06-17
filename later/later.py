import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor


_pool = None


def start():
    global _pool
    if _pool is None:
        _pool = ProcessPoolExecutor(mp.cpu_count()+2)


def async(fn, *args):
    """
    Will execute the input function asynchronously with it's input args.
    Returns a function (wrapper) that takes a callback. The wrapper function will
    call the callback with the result of the input function (fn) or an error if one should arise.

    :param fn: A function which takes zero to many args
    :param args: argument list
    :return: a function that takes a callback
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
