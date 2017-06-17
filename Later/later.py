import multiprocessing as mp
import asyncio
_pool = None
from concurrent.futures import ProcessPoolExecutor, wait

def start():
    global _pool
    if _pool is None:
        _pool = ProcessPoolExecutor(mp.cpu_count()+2)


def async(fn, *args):
    """
    :param fn:
    :param args:
    :return:
    """

    global _pool

    if _pool is None:
        start()

    future = _pool.submit(fn, *args)

    def wrapper(callback):
        future.add_done_callback(callback)

    return wrapper


def _resolve(future):

    try:
        while not future.done():
            continue
        val = future.result()
        return val, None
    except Exception as e:
        return None, e
