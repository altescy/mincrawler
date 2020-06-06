import tempfile
from pathlib import Path

from mincrawler.item import Item
from mincrawler.pipelines.stages import StoreItem
from mincrawler.storages import FileStorage


class TestStoreItem:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.item = Item("123", {"x": 456})

    def test_store_item(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            storage = FileStorage(root)
            pipeline = StoreItem(storage, "test")

            pipeline(self.item)

            assert (root / "test" / self.item.id).exists()

    @staticmethod
    def test_overwrite_false():
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            storage = FileStorage(root)
            pipeline = StoreItem(storage, "test", overwrite=False)

            item = Item("123", {"x": 456})
            pipeline(item)

            item = Item("123", {"x": 789})
            pipeline(item)

            stored_item = storage.get("test", "123")
            assert stored_item["x"] == 456

    @staticmethod
    def test_overwrite_true():
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            storage = FileStorage(root)
            pipeline = StoreItem(storage, "test", overwrite=True)

            item = Item("123", {"x": 456})
            pipeline(item)

            item = Item("123", {"x": 789})
            pipeline(item)

            stored_item = storage.get("test", "123")
            assert stored_item["x"] == 789
