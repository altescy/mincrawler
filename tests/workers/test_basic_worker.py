import os
from pathlib import Path
import tempfile

from mincrawler.crawlers.twitter import TwittwerTweetSearchCrawler
from mincrawler.pipelines.stages import StoreItem
from mincrawler.pipelines.executors import BasicPipelineExecutor
from mincrawler.storages import FileStorage
from mincrawler.workers import BasicWorker


class TestBasicWorker:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.auth_tokens = {
            "client_id": os.environ["TWITTER_CLIENT_ID"],
            "client_secret": os.environ["TWITTER_CLIENT_SECRET"],
            "token": os.environ["TWITTER_TOKEN"],
            "token_secret": os.environ["TWITTER_TOKEN_SECRET"],
        }

    def test_basic_worker(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            crawler = TwittwerTweetSearchCrawler(q="python",
                                                 count=3,
                                                 lang="ja",
                                                 locale="ja",
                                                 result_type="recent",
                                                 max_requests=1,
                                                 **self.auth_tokens)
            pipeline = BasicPipelineExecutor(
                [StoreItem(FileStorage(root), "tweets")])
            worker = BasicWorker(crawler, pipeline)

            worker()
