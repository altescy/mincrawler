import os
from mincrawler.crawlers.twitter import TwittwerTweetCrawler


class TestTwitterTweetCrawler:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.auth_tokens = {
            "client_id": os.environ["TWITTER_CLIENT_ID"],
            "client_secret": os.environ["TWITTER_CLIENT_SECRET"],
            "token": os.environ["TWITTER_TOKEN"],
            "token_secret": os.environ["TWITTER_TOKEN_SECRET"],
        }

    def test_crawl(self):
        crawler = TwittwerTweetCrawler(q="from:altescy",
                                       count=1,
                                       max_requests=1,
                                       **self.auth_tokens)
        tweets = crawler._crawl()  # pylint:disable=protected-access
        assert len(tweets) == 1
