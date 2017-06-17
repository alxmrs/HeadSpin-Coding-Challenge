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

    res = _pool.apply_async(fn, args)

    def wrapper(callback):
        res.wait()
        result = _resolve(res)
        return callback(*result)

    return wrapper


def _resolve(res):

    try:
        val = res.get()
        return val, None
    except Exception as e:
        return None, e
