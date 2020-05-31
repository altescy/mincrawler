import os
from mincrawler.crawlers.youtube import YouTubeChannelVideoCrawler


class TestYouTubeVideoCrawler:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.channels = ["UCem2GdGs8eJQbMp6GzH_hKg"]
        self.apikey = os.environ["YOUTUBE_API_KEY"]

    def test_crawl(self):
        crawler = YouTubeChannelVideoCrawler(self.apikey, self.channels)
        _video = crawler()
