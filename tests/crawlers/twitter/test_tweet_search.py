import os
from mincrawler.crawlers.twitter import TwittwerTweetSearchCrawler


class TestTwitterTweetSearchCrawler:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.auth_tokens = {
            "client_id": os.environ["TWITTER_CLIENT_ID"],
            "client_secret": os.environ["TWITTER_CLIENT_SECRET"],
            "token": os.environ["TWITTER_TOKEN"],
            "token_secret": os.environ["TWITTER_TOKEN_SECRET"],
        }

    def test_crawl(self):
        crawler = TwittwerTweetSearchCrawler(q="python",
                                             count=1,
                                             max_requests=1,
                                             **self.auth_tokens)
        tweets = list(crawler._crawl())  # pylint:disable=protected-access
        assert len(tweets) == 1
