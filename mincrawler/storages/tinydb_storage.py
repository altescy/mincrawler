from tinydb import TinyDB, where

from mincrawler.item import Item
from mincrawler.storages.storage import Storage
from mincrawler.storages.storage import ItemDuplicationError, ItemNotFoundError


@Storage.register("tinydb")
class TinyDBStorage(Storage):
    def __init__(self, path: str) -> None:
        self._path = path
        self._db = TinyDB(path)

    def insert(self, collection: str, item: Item) -> None:
        if self.exists(collection, item):
            raise ItemDuplicationError(f"Item id {item.id} already exists.")

        table = self._db.table(collection)
        table.insert(item.to_dict())

    def upsert(self, collection: str, item: Item) -> None:
        table = self._db.table(collection)
        table.upsert(item.to_dict(), where(Item.ITEM_ID_KEY) == item.id)

    def exists(self, collection: str, item: Item) -> bool:
        table = self._db.table(collection)
        items = table.search(where(Item.ITEM_ID_KEY) == item.id)
        return len(items) > 0

    def get(self, collection: str, item_id: str) -> Item:
        table = self._db.table(collection)
        item_dicts = table.search(where(Item.ITEM_ID_KEY) == item_id)
        if len(item_dicts) < 1:
            raise ItemNotFoundError(f"Item ( {item_id} ) not found.")

        return Item.from_dict(item_dicts[0])
