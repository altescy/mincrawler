import argparse
from pathlib import Path

import colt

from mincrawler import __version__
from mincrawler.utils.jsonnet import load_jsonnet
from mincrawler.workers.worker import Worker


def main(prog: str = None):
    parser = argparse.ArgumentParser(description="mincrawler",
                                     usage='%(prog)s',
                                     prog=prog)
    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s " + __version__)
    parser.add_argument(
        "config_path",
        type=str,
        help="path to parameter file describing the crawler settings")
    parser.add_argument("--module",
                        type=str,
                        action="append",
                        default=[],
                        help="additional modules to include")

    args = parser.parse_args()

    config = load_jsonnet(args.config_path)
    colt.import_modules(args.module)

    worker = colt.build(config)

    assert isinstance(worker, Worker)

    worker()
