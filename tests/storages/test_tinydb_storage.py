from concurrent.futures import ThreadPoolExecutor, as_completed
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

    @staticmethod
    def test_multithread():
        def task(path, taskid):
            storage = TinyDBStorage(path)
            with storage as s:
                s.insert("test", Item(str(taskid), {"task": taskid}))
            return taskid

        with tempfile.TemporaryDirectory() as root:
            path = root + "/test.json"
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(task, path, taskid) for taskid in range(10)
                ]
                for future in as_completed(futures):
                    taskid = future.result()
                    print(f"Task {taskid} done.")

            storage = TinyDBStorage(path)
            item = storage.get("test", "1")
            assert item["task"] == 1
