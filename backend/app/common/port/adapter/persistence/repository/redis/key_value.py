from __future__ import annotations

import abc
from dataclasses import dataclass
from enum import Enum


@dataclass(init=True, unsafe_hash=True, frozen=True)
class KeyValue[T](abc.ABC):
    class Type(Enum):
        STRING = 'string'
        # HASH = 'hash'
        # LIST = 'list'
        # SET = 'set'
        # SORTED_SET = 'sorted_set'

    type: Type
    key: str
    value: str | int | float | dict | bytes | memoryview
    ttl_seconds: int | None = None

    @staticmethod
    @abc.abstractmethod
    def create(entity: T) -> KeyValue:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_(payload: str | int | float | dict | bytes | memoryview) -> KeyValue:
        pass

    @abc.abstractmethod
    def to_entity(self) -> T:
        pass
