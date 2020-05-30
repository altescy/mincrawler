import typing as tp

from mincrawler.item import Item


class Crawler:
    def __call__(self) -> tp.Iterator[Item]:
        return self._run()

    def _run(self) -> tp.Iterator[Item]:
        raise NotImplementedError
