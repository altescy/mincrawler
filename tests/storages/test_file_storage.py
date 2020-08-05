from pathlib import Path
import tempfile

from mincrawler.item import Item
from mincrawler.storages import FileStorage


class TestFileStorage:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.data = [
            Item("123", {"text": "foo"}),
            Item("456", {"text": "bar"})
        ]

    def test_insert(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            storage = FileStorage(root)
            storage.insert_many("test", self.data)

            assert (root / "test" / "123").exists()
            assert (root / "test" / "456").exists()

    def test_update(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            storage = FileStorage(root)
            storage.insert_many("test", self.data)

            new_data = [
                Item("123", {"text": "xfoo"}),
                Item("456", {"text": "xbar"})
            ]

            storage.update_many("test", new_data)

            assert storage.get("test", "123")["text"] == "xfoo"
            assert storage.get("test", "456")["text"] == "xbar"
