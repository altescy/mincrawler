import concurrent.futures
import logging
import typing as tp

import httpx

from mincrawler.crawlers.crawler import Crawler
from mincrawler.item import Item

logger = logging.getLogger(__name__)


@Crawler.register("single_page")
class SinglePageCrawler(Crawler):
    def __init__(self,
                 requests: tp.List[tp.Dict[str, tp.Any]],
                 max_workers: int = 3) -> None:
        self._requests = requests
        self._max_workers = max_workers

    def _run(self) -> tp.Iterator[Item]:
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self._max_workers) as executor:
            futures = [
                executor.submit(httpx.get, req) for req in self._requests
            ]

            for future in concurrent.futures.as_completed(futures):
                response = future.result()

                if response.status_code != 200:
                    logger.error("[status %i] failed to fetch data from %s",
                                 response.status_code, response.url)
                    continue

                yield self._get_item(response)

    @staticmethod
    def _get_item(response: httpx.Response) -> Item:
        item_id = str(response.url)
        content = {"text": response.text}
        return Item(item_id, content)
