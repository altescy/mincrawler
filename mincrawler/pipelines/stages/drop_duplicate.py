import typing as tp

from mincrawler.item import Item
from mincrawler.pipelines.stages.stage import PipelineStage
from mincrawler.storages.storage import Storage


@PipelineStage.register("drop_duplicate")
class DropDuplicate(PipelineStage):
    def __init__(self, storage: Storage, collection: str) -> None:
        self._storage = storage
        self._collection = collection

    def _run(self, item: Item) -> tp.Optional[Item]:
        collection = self._collection

        with self._storage as storage:
            if storage.exists(collection, item):
                return None

        return item
