from collections import UserDict

from readerwriterlock import rwlock


class RWLockedDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = rwlock.RWLockFair()

    def __getitem__(self, key):
        with self._lock.gen_rlock():
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        with self._lock.gen_wlock():
            super().__setitem__(key, value)

    def __delitem__(self, key):
        with self._lock.gen_wlock():
            super().__delitem__(key)

    def __contains__(self, key):
        with self._lock.gen_rlock():
            return super().__contains__(key)

    def __iter__(self):
        with self._lock.gen_rlock():
            return super().__iter__()

    def __len__(self):
        with self._lock.gen_rlock():
            return super().__len__()

    def clear(self):
        with self._lock.gen_wlock():
            super().clear()

    # Use this to safely perform compound actions or iterate
    def locked_context(self):
        return self._lock
