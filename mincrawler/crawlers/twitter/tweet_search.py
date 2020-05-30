import copy
import logging
import typing as tp
from urllib.parse import urlencode

import colt
import httpx
from authlib.integrations.httpx_client import OAuth1Auth

from mincrawler.crawlers.crawler import Crawler
from mincrawler.item import Item

logger = logging.getLogger(__name__)


@colt.register("twitter_tweet_search")
class TwittwerTweetSearchCrawler(Crawler):
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

    def _run(self) -> tp.Iterator[Item]:
        for tweets in self._crawl():
            for tweet in tweets:
                item_id = str(tweet["id"])
                content = tweet
                yield Item(item_id, content)

    def _get_url(self, params: tp.Dict[str, tp.Any] = None) -> str:
        if params is None:
            params = self._params

        base_url = self.TWEET_SEARCH_URL.format(version=self._version)
        query_string = urlencode(params)

        return f"{base_url}?{query_string}"

    def _get_max_requests(self) -> tp.Union[int, float]:
        if self._max_requests is None or self._max_requests < 0:
            return float("inf")
        return self._max_requests

    def _crawl(self) -> tp.Iterator[tp.List[tp.Dict[str, tp.Any]]]:
        max_requests = self._get_max_requests()
        params = copy.deepcopy(self._params)

        num_requests = 0
        url = self._get_url(params)
        while num_requests < max_requests:
            logger.debug("request url: %s", url)

            response = httpx.get(url, auth=self._auth)
            logger.debug("status code: %s", response.status_code)

            tweets = response.json()["statuses"]
            meta = response.json()["search_metadata"]
            logger.debug("tweet ids: %s",
                         ", ".join(str(x["id"]) for x in tweets))

            yield tweets

            if "next_results" not in meta:
                break

            url = self.TWEET_SEARCH_URL.format(version=self._version) \
                    + meta["next_results"]
            num_requests += 1
