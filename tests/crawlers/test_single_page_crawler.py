from mincrawler.crawlers import SinglePageCrawler


class TestSinglePageCrawler:
    def setup(self):
        # pylint:disable=attribute-defined-outside-init
        self.requests = [
            {
                "url": "https://www.example.org"
            },
        ]

    def test_single_page_crawler(self):
        crawler = SinglePageCrawler(self.requests)
        crawler()
