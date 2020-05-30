import tempfile

from mincrawler.item import Item
from mincrawler.storages import TinyDBStorage


class TestFileStorage:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.data = [
            Item("123", {"text": "foo"}),
            Item("456", {"text": "bar"})
        ]

    def test_insert(self):
        with tempfile.TemporaryDirectory() as root:
            storage = TinyDBStorage(root + "/test.json")
            storage.insert_many("test", self.data)

            assert storage.get("test", "123")["text"] == "foo"
            assert storage.get("test", "456")["text"] == "bar"
