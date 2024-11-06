from __future__ import annotations

import datetime
from dataclasses import dataclass

from crawler.domain.model.data import Data


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Date(Data):
    _name: str
    yyyy_mm_dd: datetime.date

    def __init__(self, name: str, value: datetime.date):
        super().__setattr__("_name", name)
        super().__setattr__("yyyy_mm_dd", value)

    @staticmethod
    def new(value: tuple[str, datetime.date]) -> Date:
        name = value[0]
        value = value[1]
        return Date(name, value)

    def name(self) -> str:
        return self._name

    def value(self) -> datetime.date:
        return self.yyyy_mm_dd
