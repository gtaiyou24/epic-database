from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from crawler.domain.model.data import DataSet
from crawler.domain.model.interim import Id
from crawler.domain.model.url import URLSet


@dataclass(init=True, unsafe_hash=False, frozen=True)
class InterimPayload:
    """スクレイピングしたデータをまとめたオブジェクト"""
    class Type(Enum):
        COMPANY = 'company'
        JOB = 'job'

    id: Id
    type: Type
    sources: URLSet
    dataset: DataSet

    def __hash__(self):
        return hash(f"{self.id.value}-{self.type.name}")

    def __eq__(self, other: InterimPayload) -> bool:
        if not isinstance(other, InterimPayload):
            return False
        return self.id == other.id and self.type == other.type
