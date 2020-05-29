import datetime
import json
import logging
import typing as tp
import uuid
from pathlib import Path

import colt

from mincrawler.storages.storage import Storage

logger = logging.getLogger(__name__)


@colt.register("file_storage")
class FileStorage(Storage):
    def __init__(self,
                 path: tp.Union[Path, str],
                 unique_key: str = None,
                 exist_ok: bool = False):
        self._path = Path(path)
        self._unique_key = unique_key
        self._exist_ok = exist_ok

        self.path.mkdir(exist_ok=True)

    def __repr__(self) -> str:
        return f"<FileStorage: path={self.path}>"

    @property
    def path(self) -> Path:
        return self._path

    def get_unique_filename(self) -> str:
        while True:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")
            unique_id = uuid.uuid4().hex
            name = f"{timestamp}_{unique_id}"

            if not (self.path / name).exists():
                return name

    def insert(self, data: tp.List[tp.Dict[str, tp.Any]]) -> None:

        for item in data:
            if self._unique_key is None:
                filename = self.get_unique_filename()
            else:
                filename = str(item[self._unique_key])

            path = self.path / filename

            if not self._exist_ok and path.exists():
                continue

            with open(self.path / filename, "w") as f:
                json.dump(item, f)

            logger.debug("save file: %s", str(path))
