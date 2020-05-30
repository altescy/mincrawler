import os
from mincrawler.crawlers.youtube import YouTubeVideoCrawler


class TestYouTubeVideoCrawler:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.channels = ["UCem2GdGs8eJQbMp6GzH_hKg"]
        self.apikey = os.environ["YOUTUBE_API_KEY"]

    def test_crawl(self):
        crawler = YouTubeVideoCrawler(self.channels, self.apikey)
        _video = crawler()
