#!/usr/bin/env python
import logging
import os
import sys

import colt

if os.environ.get("MINCRAWLER_DEBUG"):
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO

sys.path.insert(
    0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=LEVEL)

from mincrawler.cli import main  # pylint: disable=wrong-import-position


def run():
    colt.import_modules(["mincrawler"])
    main(prog="mincrawler")


if __name__ == "__main__":
    run()
