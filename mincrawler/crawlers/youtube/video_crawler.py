import concurrent.futures
import logging
import typing as tp

import colt

from mincrawler.crawlers.youtube.youtube_crawler import YouTubeCrawler
from mincrawler.item import Item
from mincrawler.utils.batch import generate_batch

logger = logging.getLogger(__name__)


@colt.register("youtube_channel_video_crawler")
class YouTubeChannelVideoCrawler(YouTubeCrawler):
    def __init__(self,
                 apikey: str,
                 channels: tp.List[str],
                 max_workers: int = 1,
                 version: str = "v3",
                 max_results: int = 5,
                 max_requests: int = None) -> None:
        super().__init__(apikey, version, max_results, max_requests)
        self._channel_ids = channels
        self._max_workers = max_workers

    @staticmethod
    def _build_item(video_dict: tp.Dict[str, tp.Any]) -> Item:
        item_id = video_dict["id"]
        content = video_dict
        return Item(item_id, content)

    def _run(self) -> tp.Iterator[Item]:
        channels: tp.List[tp.Dict[str, tp.Any]] = []
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self._max_workers) as executor:
            futures: tp.List[concurrent.futures.Future] = []

            for batch_ids in generate_batch(self._channel_ids,
                                            self._max_results):
                future = executor.submit(self._get_channel_batch,
                                         id=",".join(batch_ids))
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                channels.extend(future.result())

        playlist_ids = [
            channel["contentDetails"]["relatedPlaylists"]["uploads"]
            for channel in channels
        ]

        video_ids = [
            playlist_item["snippet"]["resourceId"]["videoId"]
            for playlist_id in playlist_ids
            for playlist_item in self._get_playlist_items(
                playlistId=playlist_id)
        ]

        videos: tp.List[tp.Dict[str, tp.Any]] = []
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self._max_workers) as executor:
            futures = []

            for batch_ids in generate_batch(video_ids, self._max_results):
                future = executor.submit(self._get_video_batch,
                                         id=",".join(batch_ids))
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                videos.extend(future.result())

        for video_dict in videos:
            yield self._build_item(video_dict)
