import concurrent.futures
import copy
import typing as tp

from googleapiclient.discovery import build

from mincrawler.crawlers.crawler import Crawler
from mincrawler.item import Item
from mincrawler.utils.batch import generate_batch


class YouTubeCrawler(Crawler):
    API_SERVICE_NAME = "youtube"

    def __init__(self,
                 apikey: str,
                 version: str = "v3",
                 max_results: int = 5,
                 max_requests: int = None,
                 max_workers: int = 1):
        self._apikey = apikey
        self._version = version
        self._api = build(self.API_SERVICE_NAME, version, developerKey=apikey)
        self._max_results = max_results
        self._max_requests = max_requests
        self._max_workers = max_workers

    def _run(self) -> tp.Iterator[Item]:
        raise NotImplementedError

    def _get_list(self, resource,
                  **kwargs) -> tp.Iterator[tp.Dict[str, tp.Any]]:
        if "part" not in kwargs:
            kwargs["part"] = "id,snippet,contentDetails"

        if "maxResults" not in kwargs:
            kwargs["maxResults"] = self._max_results

        num_requests = 0
        max_requests = self._max_requests or float("inf")

        resource = copy.deepcopy(resource)
        request = resource.list(**kwargs)
        while request and num_requests < max_requests:
            response = request.execute()
            for item in response["items"]:
                yield tp.cast(tp.Dict[str, tp.Any], item)

            request = resource.list_next(request, response)
            num_requests += 1

    def _get_batch(self, resource, **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        if "part" not in kwargs:
            kwargs["part"] = "id,snippet,contentDetails"

        if "maxResults" not in kwargs:
            kwargs["maxResults"] = self._max_results

        resource = copy.deepcopy(resource)
        response = resource.list(**kwargs).execute()

        return tp.cast(tp.List[tp.Dict[str, tp.Any]], response["items"])

    def _get_videos(self, **kwargs) -> tp.Iterator[tp.Dict[str, tp.Any]]:
        resource = getattr(self._api, "videos")()
        yield from self._get_list(resource, **kwargs)

    def _get_channels(self, **kwargs) -> tp.Iterator[tp.Dict[str, tp.Any]]:
        resource = getattr(self._api, "channels")()
        yield from self._get_list(resource, **kwargs)

    def _get_playlist_items(self,
                            **kwargs) -> tp.Iterator[tp.Dict[str, tp.Any]]:
        resource = getattr(self._api, "playlistItems")()
        yield from self._get_list(resource, **kwargs)

    def _get_video_batch(self, **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        resource = getattr(self._api, "videos")()
        return self._get_batch(resource, **kwargs)

    def _get_channel_batch(self, **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        resource = getattr(self._api, "channels")()
        return self._get_batch(resource, **kwargs)

    def _get_playlist_item_batch(self,
                                 **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        resource = getattr(self._api, "playlistItems")()
        return self._get_batch(resource, **kwargs)

    def _exec_batch(self,
                    func: tp.Callable[..., tp.List[tp.Dict[str, tp.Any]]],
                    ids: tp.List[str],
                    batch_size: int = None,
                    **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        batch_size = batch_size or self._max_results

        items: tp.List[tp.Dict[str, tp.Any]] = []

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self._max_workers) as executor:
            futures: tp.List[concurrent.futures.Future] = []

            for batch_ids in generate_batch(ids, batch_size):
                future = executor.submit(func,
                                         id=",".join(batch_ids),
                                         **kwargs)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                items.extend(future.result())

        return items
