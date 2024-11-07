from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from crawler.domain.model.interim import InterimId
from crawler.domain.model.url import URLSet


@dataclass(init=True, unsafe_hash=False, frozen=True)
class Interim:
    """スクレイピングしたデータをまとめたオブジェクト"""
    class Source(Enum):
        GBIZINFO = 'gBizInfo'
        JOB = 'job'

    id: InterimId
    source: Source
    from_urls: URLSet
    payload: dict[str, Any]

    def __hash__(self):
        return hash(f"{self.id.value}-{self.source.name}")

    def __eq__(self, other: Interim) -> bool:
        if not isinstance(other, Interim):
            return False
        return self.id == other.id and self.source == other.source

    def get(self, key: str) -> Any | None:
        value = self.payload
        for k in key.split("."):
            if value is None or k not in value.keys():
                return None
            value = value[k]
        return value

    def set_payload(self, payload: dict[str, Any]) -> Interim:
        return Interim(self.id, self.source, self.from_urls, payload)
