import colt

from mincrawler.workers.worker import Worker


@colt.register("basic_worker")
class BasicWorker(Worker):
    def _run(self) -> None:
        self._crawler(self._storage)
