import typing as tp

import colt

from mincrawler.crawlers.crawler import Crawler
from mincrawler.pipelines.pipeline import Pipeline
from mincrawler.workers.worker import Worker


@colt.register("basic_worker")
class BasicWorker(Worker):
    def __init__(self,
                 crawler: Crawler,
                 pipelines: tp.List[Pipeline] = None,
                 max_workers: int = 3) -> None:
        super().__init__(crawler, pipelines)
        self._max_workers = max_workers

    def _run(self) -> None:
        # from concurrent.futures import ThreadPoolExecutor
        # with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
        #     for item in self._crawler():
        #         executor.submit(self._run_pipeline, item)
        for item in self._crawler():
            self._run_pipeline(item)
