import typing as tp

from mincrawler.crawlers.crawler import Crawler
from mincrawler.item import Item
from mincrawler.pipelines.pipeline import Pipeline


class Worker:
    def __init__(self,
                 crawler: Crawler,
                 pipelines: tp.List[Pipeline] = None) -> None:
        self._crawler = crawler
        self._pipelines = pipelines or []

    def __call__(self) -> None:
        self._run()

    def _run(self) -> None:
        raise NotImplementedError

    def _run_pipeline(self, item: tp.Optional[Item]) -> None:
        for stage in self._pipelines:
            item = stage(item)
