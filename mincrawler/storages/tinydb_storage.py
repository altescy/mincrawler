from __future__ import annotations
import os
from threading import Lock
import typing as tp

from tinydb import TinyDB, where
from tinyrecord import transaction

from mincrawler.item import Item
from mincrawler.storages.storage import Storage
from mincrawler.storages.storage import ItemDuplicationError, ItemNotFoundError
from mincrawler.utils.locked_dict import LockedDict


@Storage.register("tinydb")
class TinyDBStorage(Storage):
    _locks: LockedDict[str, tp.Tuple[Lock, TinyDB]] = LockedDict()

    def __init__(self, path: str) -> None:
        path = os.path.normpath(os.path.abspath(path))

        with TinyDBStorage._locks as locks:
            if path not in locks:
                locks[path] = Lock(), TinyDB(path)
            self._lock, self._db = locks[path]

    def __enter__(self) -> TinyDBStorage:
        self._lock.acquire()
        return self

    def __exit__(self, *args) -> None:
        self._lock.release()

    def insert(self, collection: str, item: Item) -> None:
        if self.exists(collection, item):
            raise ItemDuplicationError(f"Item id {item.id} already exists.")

        table = self._db.table(collection)
        with transaction(table) as tx:
            tx.insert(item.to_dict())

    def update(self, collection: str, item: Item) -> None:
        if not self.exists(collection, item):
            raise ItemNotFoundError(f"Item ( {item.id} ) not found.")

        table = self._db.table(collection)
        with transaction(table) as tx:
            tx.update(item.to_dict(), where(Item.ITEM_ID_KEY) == item.id)

    def upsert(self, collection: str, item: Item) -> None:
        if self.exists(collection, item):
            self.update(collection, item)
        else:
            self.insert(collection, item)

    def exists(self, collection: str, item: Item) -> bool:
        table = self._db.table(collection)
        exists = table.contains(where(Item.ITEM_ID_KEY) == item.id)
        return tp.cast(bool, exists)

    def get(self, collection: str, item_id: str) -> Item:
        table = self._db.table(collection)
        item_dict = table.get(where(Item.ITEM_ID_KEY) == item_id)
        if item_dict is None:
            raise ItemNotFoundError(f"Item ( {item_id} ) not found.")

        return Item.from_dict(item_dict)
