from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from crawler.domain.model.data import DataSet
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

    def get(self, key: str, default: Any | None = None) -> Any | None:
        value = self.payload
        for k in key.split("."):
            if value is None or k not in list(value):
                return default
            value = value[k]
        return value

    def set(self, key: str, value: Any) -> Interim:
        payload = self.payload
        payload[key] = value
        return Interim(self.id, self.source, self.from_urls, payload)

    def set_with_dataset(self, dataset: DataSet) -> Interim:
        interim = self
        for key, value in dataset.to_dict().items():
            interim = interim.set(key, value)
        return interim

    def set_payload(self, payload: dict[str, Any]) -> Interim:
        return Interim(self.id, self.source, self.from_urls, payload)
