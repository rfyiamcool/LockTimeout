# coding:utf-8
import random
import time
import threading
from mutex_timeout import TimeoutLock


def locking_thread_fn(name, lock, duration, timeout):
    with TimeoutLock(name, lock, timeout=timeout):
        time.sleep(duration)


def test_lock():
    _lock = TimeoutLock.lock()

    _threads = []
    _total_d = 0
    for i in range(3):
        _d = random.random() * 3
        _to = random.random() * 2
        _threads.append(threading.Thread(
            target=locking_thread_fn, args=('thread%d' % i, _lock, _d, _to)))
        _total_d += _d

    _t = time.time()

    for t in _threads:
        t.start()

    for t in _threads:
        t.join()

    _t = time.time() - _t

    print('duration: %.2f sec / expected: %.2f (%.1f%%)'
          % (_t, _total_d, 100 / _total_d * _t))


if __name__ == "__main__":
    test_lock()
