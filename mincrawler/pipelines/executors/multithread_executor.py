import concurrent.futures
import typing as tp

from mincrawler.item import Item
from mincrawler.pipelines.executors.executor import PipelineExecutor
from mincrawler.pipelines.stages.stage import PipelineStage


@PipelineExecutor.register("multi_thread")
class MultiThreadPipelineExecutor(PipelineExecutor):
    def __init__(self, stages: tp.List[PipelineStage], max_workers: int = 3):
        super().__init__(stages)
        self._max_workers = max_workers

    def _run(self, items: tp.Iterable[Item]) -> None:
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self._max_workers) as executor:
            futures = [
                executor.submit(self._run_pipeline, item) for item in items
            ]

            for future in concurrent.futures.as_completed(futures):
                future.result()
