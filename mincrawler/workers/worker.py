import colt

from mincrawler.crawlers.crawler import Crawler
from mincrawler.pipelines.executors.executor import PipelineExecutor


class Worker(colt.Registrable):
    def __init__(self, crawler: Crawler, pipeline: PipelineExecutor) -> None:
        self._crawler = crawler
        self._pipeline = pipeline

    def __call__(self) -> None:
        self._run()

    def _run(self) -> None:
        raise NotImplementedError
