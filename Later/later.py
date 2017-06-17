import multiprocessing as mp
import asyncio
_pool = None


def start():
    global _pool
    if _pool is None:
        _pool = mp.Pool(mp.cpu_count() + 2)


def async(fn, *args):
    """
    :param fn:
    :param args:
    :return:
    """

    global _pool

    if _pool is None:
        start()

    def wrapper(callback):
        val_cb = lambda x: callback(x, None)
        err_cb = lambda e: callback(None, e)

        try:
            _pool.apply_async(fn, args, callback=val_cb, error_callback=err_cb)
        except Exception as e:
            return callback(None, e)

    return wrapper

