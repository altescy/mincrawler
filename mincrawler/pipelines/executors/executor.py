import typing as tp

import colt

from mincrawler.item import Item
from mincrawler.pipelines.stages.stage import PipelineStage


class PipelineExecutor(colt.Registrable):
    def __init__(self, stages: tp.List[PipelineStage]):
        self._stages = stages

    def __call__(self, items: tp.Iterable[Item]) -> None:
        self._run(items)

    def _run(self, items: tp.Iterable[Item]) -> None:
        raise NotImplementedError

    def _run_pipeline(self, item: tp.Optional[Item]) -> None:
        for stage in self._stages:
            item = stage(item)
            if item is None:
                break
