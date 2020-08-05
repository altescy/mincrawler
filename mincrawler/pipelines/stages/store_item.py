import typing as tp

from mincrawler.item import Item
from mincrawler.pipelines.stages.stage import PipelineStage
from mincrawler.storages.storage import Storage


@PipelineStage.register("store_item")
class StoreItem(PipelineStage):
    def __init__(self,
                 storage: Storage,
                 collection: str,
                 overwrite: bool = False) -> None:
        self._storage = storage
        self._collection = collection
        self._overwrite = overwrite

    def _run(self, item: Item) -> tp.Optional[Item]:
        with self._storage as storage:
            item_exists = self._storage.exists(self._collection, item)

            if self._overwrite or not item_exists:
                storage.upsert(self._collection, item)

        return item
