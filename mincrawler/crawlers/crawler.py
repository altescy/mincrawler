import typing as tp

import colt

from mincrawler.item import Item


class Crawler(colt.Registrable):
    def __call__(self) -> tp.Iterator[Item]:
        return self._run()

    def _run(self) -> tp.Iterator[Item]:
        raise NotImplementedError
