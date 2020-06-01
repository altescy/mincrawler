import typing as tp

import colt

from mincrawler.item import Item


class Pipeline(colt.Registrable):
    def __call__(self, item: tp.Optional[Item]) -> tp.Optional[Item]:
        if item is None:
            return None
        return self._run(item)

    def _run(self, item: Item) -> tp.Optional[Item]:
        raise NotImplementedError
