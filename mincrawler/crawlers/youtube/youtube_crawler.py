import copy
import typing as tp

from apiclient.discovery import build
from googleapiclient.discovery import Resource
from googleapiclient.http import HttpRequest

from mincrawler.crawlers.crawler import Crawler
from mincrawler.item import Item


class YouTubeCrawler(Crawler):
    API_SERVICE_NAME = "youtube"

    def __init__(self,
                 apikey: str,
                 version: str = "v3",
                 max_results: int = 5,
                 max_requests: int = None):
        self._apikey = apikey
        self._version = version
        self._api = build(self.API_SERVICE_NAME, version, developerKey=apikey)
        self._max_results = max_results
        self._max_requests = max_requests

    def _run(self) -> tp.Iterator[Item]:
        raise NotImplementedError

    def _get_list(self, resource: Resource,
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

    def _get_batch(self, resource: Resource,
                   **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        if "part" not in kwargs:
            kwargs["part"] = "id,snippet,contentDetails"

        if "maxResults" not in kwargs:
            kwargs["maxResults"] = self._max_results

        resource = copy.deepcopy(resource)
        response = resource.list(**kwargs).execute()

        return tp.cast(tp.List[tp.Dict[str, tp.Any]], response["items"])

    def _get_videos(self, **kwargs) -> tp.Iterator[tp.Dict[str, tp.Any]]:
        yield from self._get_list(self._api.videos(), **kwargs)

    def _get_channels(self, **kwargs) -> tp.Iterator[tp.Dict[str, tp.Any]]:
        yield from self._get_list(self._api.channels(), **kwargs)

    def _get_playlist_items(self,
                            **kwargs) -> tp.Iterator[tp.Dict[str, tp.Any]]:
        yield from self._get_list(self._api.playlistItems(), **kwargs)

    def _get_video_batch(self, **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        return self._get_batch(self._api.videos(), **kwargs)

    def _get_channel_batch(self, **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        return self._get_batch(self._api.channels(), **kwargs)

    def _get_playlist_item_batch(self,
                                 **kwargs) -> tp.List[tp.Dict[str, tp.Any]]:
        return self._get_batch(self._api.playlistItems(), **kwargs)
