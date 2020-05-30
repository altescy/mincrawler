import colt

from mincrawler.workers.worker import Worker


@colt.register("basic_worker")
class BasicWorker(Worker):
    def _run(self) -> None:
        for item in self._crawler():
            self._run_pipeline(item)
