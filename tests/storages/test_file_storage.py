from pathlib import Path
import tempfile

from mincrawler.storages import FileStorage


class TestFileStorage:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.data = [{"id": 123, "text": "foo"}, {"id": 456, "text": "bar"}]

    def test_insert(self):
        with tempfile.TemporaryDirectory() as path:
            path = Path(path)

            storage = FileStorage(path, unique_key="id")
            storage.insert(self.data)

            assert (path / "123").exists()
            assert (path / "456").exists()
