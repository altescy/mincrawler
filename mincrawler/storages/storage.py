import typing as tp

import colt

from mincrawler.item import Item


class Storage(colt.Registrable):
    def insert(self, collection: str, item: Item) -> None:
        raise NotImplementedError

    def insert_many(self, collection: str, items: tp.List[Item]) -> None:
        for item in items:
            self.insert(collection, item)

    def upsert(self, collection: str, item: Item) -> None:
        raise NotImplementedError

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
