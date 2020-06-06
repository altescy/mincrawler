import typing as tp

from mincrawler.item import Item
from mincrawler.pipelines.executors.executor import PipelineExecutor


@PipelineExecutor.register("basic")
class BasicPipelineExecutor(PipelineExecutor):
    def _run(self, items: tp.Iterable[Item]) -> None:
        for item in items:
            self._run_pipeline(item)
