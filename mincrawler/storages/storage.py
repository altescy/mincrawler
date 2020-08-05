from __future__ import annotations
import typing as tp

import colt

from mincrawler.item import Item


class Storage(colt.Registrable):
    def __enter__(self) -> Storage:
        return self

    def __exit__(self, *args) -> None:
        return None

    def insert(self, collection: str, item: Item) -> None:
        raise NotImplementedError

    def insert_many(self, collection: str, items: tp.List[Item]) -> None:
        for item in items:
            self.insert(collection, item)

    def update(self, collection: str, item: Item) -> None:
        raise NotImplementedError

    def update_many(self, collection: str, items: tp.List[Item]) -> None:
        for item in items:
            self.update(collection, item)

    def upsert(self, collection: str, item: Item) -> None:
        if self.exists(collection, item):
            self.update(collection, item)
        else:
            self.insert(collection, item)

    def upsert_many(self, collection: str, items: tp.List[Item]) -> None:
        for item in items:
            self.upsert(collection, item)

    def exists(self, collection: str, item: Item) -> bool:
        raise NotImplementedError

    def get(self, collection: str, item_id: str) -> Item:
        raise NotImplementedError


class ItemDuplicationError(Exception):
    """Item Duplication Error"""


class ItemNotFoundError(Exception):
    """Item Not Found Error"""
