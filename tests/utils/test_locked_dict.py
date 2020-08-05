import threading

from mincrawler.utils.locked_dict import LockedDict


class TestLockedDict:
    @staticmethod
    def test_multithread():
        data = LockedDict()

        def task_one():
            with data as d:
                d["x"] = 123

        def task_two():
            with data as d:
                d["x"] = 456

        thread_one = threading.Thread(target=task_one)
        thread_two = threading.Thread(target=task_two)

        thread_one.start()
        thread_two.start()
