import logging
import typing as tp

from mincrawler.crawlers.crawler import Crawler
from mincrawler.crawlers.youtube.youtube_crawler import YouTubeCrawler
from mincrawler.item import Item

logger = logging.getLogger(__name__)


@Crawler.register("youtube_channel_video")
class YouTubeChannelVideoCrawler(YouTubeCrawler):
    def __init__(
            self,
            apikey: str,
            channels: tp.List[str],
            version: str = "v3",
            max_results: int = 5,
            max_requests: int = None,
            max_workers: int = 1,
    ) -> None:
        super().__init__(apikey, version, max_results, max_requests,
                         max_workers)
        self._channel_ids = channels

    @staticmethod
    def _build_item(video_dict: tp.Dict[str, tp.Any]) -> Item:
        item_id = video_dict["id"]
        content = video_dict
        return Item(item_id, content)

    def _run(self) -> tp.Iterator[Item]:
        channels = self._exec_batch(self._get_channel_batch, self._channel_ids)

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

        videos = self._exec_batch(self._get_video_batch, video_ids)

        for video_dict in videos:
            yield self._build_item(video_dict)
