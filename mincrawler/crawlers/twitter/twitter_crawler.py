import typing as tp
from urllib.parse import urlencode

from authlib.integrations.httpx_client import OAuth1Auth

from mincrawler.crawlers.crawler import Crawler
from mincrawler.item import Item


class TwitterCrawler(Crawler):
    RESOURCE_URL = ""

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 token: str,
                 token_secret: str,
                 version: str = "1.1",
                 **params) -> None:
        self._auth = OAuth1Auth(client_id, client_secret, token, token_secret)
        self._version = version
        self._params = params

    def get_url(self, params: tp.Dict[str, tp.Any] = None) -> str:
        if params is None:
            params = self._params

        base_url = self.RESOURCE_URL.format(version=self._version)
        query_string = urlencode(params)

        return f"{base_url}?{query_string}"

    def _run(self) -> tp.Iterator[Item]:
        raise NotImplementedError
