from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterator


@dataclass(init=False, unsafe_hash=False, frozen=True)
class InterimId:
    class Type(Enum):
        UUID = ('UUID', r'([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})')
        JCN = ('法人番号', r'[0-9]{13}')

        def __init__(self, ja: str, regex: str):
            self.ja = ja
            self.regex = regex

        def match(self, value: str) -> bool:
            return re.match(self.regex, value) is not None

        def make(self, value: str) -> InterimId:
            return InterimId(value, self)

    value: str
    type: Type
    other_id: InterimId | None

    def __init__(self, value: str, type: Type, other_id: InterimId | None = None):
        assert type.match(value), f"{type.ja}は{type.regex}の形式で指定してください。"
        super().__setattr__("value", value)
        super().__setattr__("type", type)
        super().__setattr__("other_id", other_id)

    def __hash__(self):
        if self.other_id is None:
            return hash(f'{self.value}{self.type.name}')
        return hash(f'{self.value}{self.type.name}{self.other_id.__hash__()}')

    def __eq__(self, other: InterimId) -> bool:
        if not isinstance(other, InterimId):
            return False

        for type in InterimId.Type:
            id = self.type_of(type)
            other_id = other.type_of(type)
            if id is None or other_id is None:
                continue
            if id.value == other_id.value:
                return True
        return False

    def __iter__(self) -> Iterator[InterimId]:
        for type in InterimId.Type:
            id = self.type_of(type)
            if id is None:
                continue
            yield id

    @staticmethod
    def of(value: str) -> InterimId:
        for type in InterimId.Type:
            if type.match(value):
                return type.make(value)
        raise ValueError('無効な企業IDです')

    def type_of(self, type: Type) -> InterimId | None:
        if self.type == type:
            return self
        if self.other_id:
            return self.other_id.type_of(type)
        return None

    def contains(self, type: Type, value: str | None = None) -> bool:
        id = self.type_of(type)
        if value is None:
            return id is not None
        return id.value == value

    def set_other_id(self, other_id: InterimId) -> InterimId:
        if self.contains(other_id.type):
            raise ValueError(f'すでに {other_id.type.name} がセットされています。')

        if self.other_id is not None:
            other_id = self.other_id.set_other_id(other_id)
        return InterimId(self.value, self.type, other_id)