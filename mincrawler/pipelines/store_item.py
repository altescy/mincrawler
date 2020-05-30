import typing as tp

import colt

from mincrawler.item import Item
from mincrawler.pipelines.pipeline import Pipeline
from mincrawler.storages.storage import Storage


@colt.register("store_item")
class StoreItem(Pipeline):
    def __init__(self,
                 storage: Storage,
                 collection: str,
                 overwrite: bool = False) -> None:
        self._storage = storage
        self._collection = collection
        self._overwrite = overwrite

    def _run(self, item: Item) -> tp.Optional[Item]:
        item_exists = self._storage.exists(self._collection, item)

        if self._overwrite or not item_exists:
            self._storage.upsert(self._collection, item)

        return item
