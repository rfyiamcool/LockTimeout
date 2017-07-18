# coding:utf-8
import threading
import time


class TimeoutLock:
    class lock:
        def __init__(self):
            self.owner = None
            self.lock = threading.Lock()
            self.cond = threading.Condition()

        def _release(self):
            self.owner = None
            self.lock.release()
            with self.cond:
                self.cond.notify()

    def __init__(self, owner, lock, timeout=1, raise_on_timeout=False):
        self._owner = owner
        self._lock = lock
        self._timeout = timeout
        self._raise_on_timeout = raise_on_timeout

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, type, value, tb):
        self.release()

    def acquire(self):
        if self._raise_on_timeout:
            if not self._waitLock():
                raise RuntimeError('"%s" could not aquire lock within %d sec'
                                   % (self._owner, self._timeout))
        else:
            while True:
                if self._waitLock():
                    break
                print('"%s" is waiting for "%s" and is getting bored...'
                      % (self._owner, self._lock.owner))
        self._lock.owner = self._owner

    def release(self):
        self._lock._release()

    def _waitLock(self):
        with self._lock.cond:
            _current_t = _start_t = time.time()
            while _current_t < _start_t + self._timeout:
                if self._lock.lock.acquire(False):
                    return True
                else:
                    self._lock.cond.wait(self._timeout - _current_t + _start_t)
                    _current_t = time.time()
        return False
