import tempfile
from pathlib import Path

from mincrawler.item import Item
from mincrawler.pipelines import DropDuplicate
from mincrawler.storages import FileStorage


class TestDropDuplicate:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.items = [
            Item("123", {"x": 123}),
            Item("456", {"x": 456}),
        ]

    def test_drop_duplicate(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            storage = FileStorage(root)

            storage.insert_many("test", self.items)

            pipeline = DropDuplicate(storage, "test")

            item = Item("123", {"x": 123})
            assert pipeline(item) is None

            item = Item("789", {"x": 789})
            assert pipeline(item) is item
