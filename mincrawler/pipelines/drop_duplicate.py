import typing as tp

from mincrawler.item import Item
from mincrawler.pipelines.pipeline import Pipeline
from mincrawler.storages.storage import Storage


@Pipeline.register("drop_duplicate")
class DropDuplicate(Pipeline):
    def __init__(self, storage: Storage, collection: str) -> None:
        self._storage = storage
        self._collection = collection

    def _run(self, item: Item) -> tp.Optional[Item]:
        collection = self._collection

        if self._storage.exists(collection, item):
            return None

        return item
