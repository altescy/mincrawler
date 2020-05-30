import logging
import typing as tp

import colt
import pafy

from mincrawler.crawlers.youtube.youtube_crawler import YouTubeCrawler
from mincrawler.item import Item

logger = logging.getLogger(__name__)


@colt.register("youtube_video_crawler")
class YouTubeVideoCrawler(YouTubeCrawler):
    def __init__(self, channels: tp.List[str], apikey: str) -> None:
        super().__init__(apikey)

        self._channels = channels

    def _run(self) -> tp.Iterator[Item]:
        for channel_id in self._channels:
            channel = pafy.get_channel(channel_id)
            for video in channel.uploads:
                item = self._build_item(video, channel)
                logger.debug("fetch video: %s", video.videoid)
                yield item

    def _build_item(self, video, channel) -> Item:
        item_id = video.videoid
        content = {
            "video": self._build_video_dict(video),
            "channel": self._build_channel_dict(channel),
        }
        return Item(item_id, content)
