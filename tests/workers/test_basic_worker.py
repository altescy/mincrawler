import os
from pathlib import Path
import tempfile

from mincrawler.crawlers.twitter import TwittwerTweetCrawler
from mincrawler.pipelines import StoreItem
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

    def test_run(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)

            crawler = TwittwerTweetCrawler(q="python",
                                           count=5,
                                           max_requests=1,
                                           **self.auth_tokens)
            pipelines = [StoreItem(FileStorage(root), "tweets")]
            worker = BasicWorker(crawler, pipelines)

            worker()

            assert len(list(root.glob("tweets/*"))) == 5
