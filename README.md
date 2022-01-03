mincrawler
==========

[![Actions Status](https://github.com/altescy/mincrawler/actions?query=workflow%3ACI)
[![License](https://img.shields.io/github/license/altescy/mincrawler)](https://github.com/altescy/mincrawler/blob/master/LICENSE)


### Installation

```
pip install git+https://github.com/altescy/mincrawler
```

### Usage

```
$ cat config.jsonnet
local storage = {
  "@type": "tinydb",
  "path": "storage.json",
};
local tweet_collection = "tweets";

{
    "@type": "basic",
    "crawler": {
        "@type": "twitter_tweet_search",
        "client_id": std.extVar("TWITTER_CLIENT_ID"),
        "client_secret": std.extVar("TWITTER_CLIENT_SECRET"),
        "token": std.extVar("TWITTER_TOKEN"),
        "token_secret": std.extVar("TWITTER_TOKEN_SECRET"),
        "q": "python",
        "lang": "en",
        "count": 10,
        "max_requests": 1,
    },
    "pipeline": {
      "@type": "basic",
      "stages": [
        {
          "@type": "drop_duplicate",
          "storage": storage,
          "collection": tweet_collection,
        },
        {
          "@type": "store_item",
          "storage": storage,
          "collection": tweet_collection,
        },
      ]
    }
}
$ mincrawler config.jsonnet
$ cat storage.json | jq ".tweets | .[].content.text"
```
