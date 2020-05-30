import typing as tp

import pafy

from mincrawler.crawlers.crawler import Crawler
from mincrawler.item import Item

VIDEO_ATTRIBUTIONS = [
    "videoid", "version", "watchv_url", "description", "likes", "dislikes",
    "category", "published", "username", "title", "rating", "author",
    "duration", "keywords", "bigthumb", "bigthumbhd", "expiry"
]
CHANNEL_ATTRIBUTIONS = [
    "channel_url", "channel_id", "title", "description", "logo",
    "subscrierCount", "title"
]


class YouTubeCrawler(Crawler):
    def __init__(self, apikey: str):
        pafy.set_api_key(apikey)

    def _run(self) -> tp.Iterator[Item]:
        raise NotImplementedError

    @staticmethod
    def _build_video_dict(video) -> tp.Dict[str, tp.Any]:
        video_dict = {
            key: getattr(video, key, None)
            for key in VIDEO_ATTRIBUTIONS
        }
        return video_dict

    @staticmethod
    def _build_channel_dict(channel) -> tp.Dict[str, tp.Any]:
        channel_dict = {
            key: getattr(channel, key, None)
            for key in CHANNEL_ATTRIBUTIONS
        }
        return channel_dict
