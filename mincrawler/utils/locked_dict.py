from __future__ import annotations
from threading import Lock
from typing import Dict, Generic, Hashable, Iterator, Optional, Tuple, TypeVar, Union

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LockedDict(Generic[K, V]):
    def __init__(self, data: Dict[K, V] = None) -> None:
        self._lock = Lock()
        self._data: Dict[K, V] = {} if data is None else data

    def __enter__(self) -> LockedDict:
        self._lock.acquire()
        return self

    def __exit__(self, *args) -> None:
        self._lock.release()

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __setitem__(self, key: K, val: V) -> None:
        self._data[key] = val

    def __iter__(self) -> Iterator[K]:
        yield from self._data

    def __repr__(self) -> str:
        return repr(self._data)

    def get(self, key: K, default: V = None) -> Optional[V]:
        return self._data.get(key, default)

    def pop(self, key: K, default: V = None) -> Optional[V]:
        return self._data.pop(key, default)

    def items(self) -> Iterator[Tuple[K, V]]:
        yield from self._data.items()

    def update(self, data: Union[LockedDict[K, V], Dict[K, V]]) -> None:
        for key, val in data.items():
            self._data[key] = val
