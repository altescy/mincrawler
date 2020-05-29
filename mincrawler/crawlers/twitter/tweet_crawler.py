import copy
import typing as tp
from urllib.parse import urlencode

import colt
import httpx
from authlib.integrations.httpx_client import OAuth1Auth

from mincrawler.crawlers.crawler import Crawler
from mincrawler.storages.storage import Storage


@colt.register("twitter_tweet_crawler")
class TwittwerTweetCrawler(Crawler):
    TWEET_SEARCH_URL = "https://api.twitter.com/{version}/search/tweets.json"

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 token: str,
                 token_secret: str,
                 max_requests: int = None,
                 version: str = "1.1",
                 **params) -> None:
        self._auth = OAuth1Auth(client_id, client_secret, token, token_secret)
        self._max_requests = max_requests
        self._version = version
        self._params = params

    def _run(self, storage: Storage) -> None:
        tweets = self._crawl()
        storage.insert(tweets)

    def _get_url(self, params: tp.Dict[str, tp.Any] = None) -> str:
        if params is None:
            params = self._params

        base_url = self.TWEET_SEARCH_URL.format(version=self._version)
        query_string = urlencode(self._params)

        return f"{base_url}?{query_string}"

    def _get_max_requests(self) -> tp.Union[int, float]:
        if self._max_requests is None or self._max_requests < 0:
            return float("inf")
        return self._max_requests

    def _crawl(self) -> tp.List[tp.Dict[str, tp.Any]]:
        max_requests = self._get_max_requests()
        params = copy.deepcopy(self._params)
        tweets: tp.List[tp.Dict[str, tp.Any]] = []

        num_requests = 0
        while num_requests < max_requests:
            url = self._get_url(params)
            response = httpx.get(url, auth=self._auth)
            data = response.json()["statuses"]

            if not data:
                return tweets

            tweets.extend(data)

            params["max_id"] = tweets[-1]["id"] - 1
            num_requests += 1

        return tweets
