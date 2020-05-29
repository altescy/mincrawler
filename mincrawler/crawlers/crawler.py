import typing as tp

from mincrawler.storages.storage import Storage


class Crawler:
    def __call__(self, storage: Storage) -> None:
        self._run(storage)

    def _run(self, storage: Storage) -> None:
        raise NotImplementedError
