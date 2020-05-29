from mincrawler.crawlers.crawler import Crawler
from mincrawler.storages.storage import Storage


class Worker:
    def __init__(self, crawler: Crawler, storage: Storage) -> None:
        self._crawler = crawler
        self._storage = storage

    def __call__(self) -> None:
        self._run()

    def _run(self) -> None:
        raise NotImplementedError
