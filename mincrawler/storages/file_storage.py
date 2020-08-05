from __future__ import annotations
import json
import logging
import os
from pathlib import Path
from threading import Lock
import typing as tp

from mincrawler.item import Item
from mincrawler.storages.storage import Storage
from mincrawler.storages.storage import ItemDuplicationError, ItemNotFoundError
from mincrawler.utils.locked_dict import LockedDict

logger = logging.getLogger(__name__)


@Storage.register("file")
class FileStorage(Storage):
    _locks: LockedDict[str, Lock] = LockedDict()

    def __init__(self, root: tp.Union[Path, str], overwrite: bool = False):
        root = os.path.normpath(os.path.abspath(str(root)))
        self._root = Path(root)
        self._overwrite = overwrite

        self.root.mkdir(exist_ok=True)

        with FileStorage._locks as locks:
            if root not in locks:
                locks[root] = Lock()
            self._lock = locks[root]

    def __repr__(self) -> str:
        return f"<FileStorage: path={self.root}>"

    def __enter__(self) -> FileStorage:
        self._lock.acquire()
        return self

    def __exit__(self, *args) -> None:
        self._lock.release()

    @property
    def root(self) -> Path:
        return self._root

    def _get_collection_path(self, collection: str) -> Path:
        return self.root / collection

    def _get_item_path(self, collection: str, item: Item) -> Path:
        return self._get_collection_path(collection) / item.id

    def _create_collection(self, collection: str) -> None:
        self._get_collection_path(collection).mkdir(exist_ok=True)

    def insert(self, collection: str, item: Item) -> None:
        self._create_collection(collection)

        path = self._get_item_path(collection, item)

        if path.exists():
            raise ItemDuplicationError(f"Item id {item.id} already exists.")

        with path.open("w") as f:
            json.dump(item.to_dict(), f)

        logger.debug("save file: %s", str(path))

    def update(self, collection: str, item: Item) -> None:
        if not self.exists(collection, item):
            raise ItemNotFoundError(f"Item ( {item.id} ) not found.")

        path = self._get_item_path(collection, item)
        with path.open("w") as f:
            json.dump(item.to_dict(), f)

    def upsert(self, collection: str, item: Item) -> None:
        self._create_collection(collection)

        path = self._get_item_path(collection, item)

        with path.open("w") as f:
            json.dump(item.to_dict(), f)

        logger.debug("save file: %s", str(path))

    def exists(self, collection: str, item: Item) -> bool:
        return self._get_item_path(collection, item).exists()

    def get(self, collection: str, item_id: str) -> Item:
        path = self._get_collection_path(collection) / item_id

        if not path.exists():
            raise ItemNotFoundError(f"Item ( {item_id} ) not found.")

        with path.open("r") as f:
            item = Item.from_dict(json.load(f))

        return item
