import os
from pathlib import Path
import tempfile

from mincrawler.crawlers.twitter import TwittwerTweetCrawler
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
        with tempfile.TemporaryDirectory() as path:
            path = Path(path)

            crawler = TwittwerTweetCrawler(q="from:altescy",
                                           count=2,
                                           max_requests=1,
                                           **self.auth_tokens)
            storage = FileStorage(path, unique_key="id")
            worker = BasicWorker(crawler, storage)

            worker()

            assert len(list(path.glob("*"))) == 2
