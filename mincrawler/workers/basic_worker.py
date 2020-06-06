from mincrawler.workers.worker import Worker


@Worker.register("basic")
class BasicWorker(Worker):
    def _run(self) -> None:
        self._pipeline(self._crawler())
