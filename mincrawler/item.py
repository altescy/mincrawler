from __future__ import annotations
import typing as tp


class Item:
    def __init__(self, item_id: str, content: tp.Dict[str, tp.Any]) -> None:
        self._item_id = item_id
        self._content = content

    @property
    def id(self) -> str:
        return self._item_id

    def __setitem__(self, key: str, value: tp.Dict[str, tp.Any]) -> None:
        self._content[key] = value

    def __getitem__(self, key: str) -> tp.Any:
        return self._content[key]

    def __delitem__(self, key: str) -> None:
        del self._content[key]

    def __iter__(self) -> tp.Iterator[str]:
        for key in self._content.keys():
            yield key

    def __len__(self) -> int:
        return len(self._content)

    def get(self, key: str, sub: tp.Any = None) -> tp.Any:
        return self._content.get(key, sub)

    def update(self, content: tp.Dict[str, tp.Any]) -> None:
        self._content.update(content)

    def to_dict(self) -> tp.Dict[str, tp.Any]:
        return {
            "item_id": self._item_id,
            "content": self._content,
        }

    @classmethod
    def from_dict(cls, item_dict: tp.Dict[str, tp.Any]) -> Item:
        return cls(
            item_id=item_dict["item_id"],
            content=item_dict["content"],
        )
