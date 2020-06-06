import copy
import typing as tp

from mincrawler.item import Item
from mincrawler.pipelines.executors import BasicPipelineExecutor
from mincrawler.pipelines.stages.stage import PipelineStage


class AddOne(PipelineStage):
    def _run(self, item: Item) -> tp.Optional[Item]:
        item["x"] += 1
        return item


class TestBasicPipelineExecutor:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.items = [Item("123", {"x": 123}), Item("456", {"x": 456})]

    def test_basic_pipeline_executor(self):
        items = copy.deepcopy(self.items)

        pipeline = BasicPipelineExecutor([AddOne()])
        pipeline(items)

        assert items[0]["x"] == 124
        assert items[1]["x"] == 457
