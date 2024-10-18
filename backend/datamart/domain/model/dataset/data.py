from dataclasses import dataclass
from typing import Any


@dataclass(init=True, unsafe_hash=True, frozen=True)
class KeyValue:
    key: str
    value: Any


@dataclass(init=False, unsafe_hash=True, frozen=True)
class DataId:
    value: str

    def __init__(self, value: str):
        assert value, "データIDは必須です。"
        super().__setattr__("value", value)


@dataclass(init=True, unsafe_hash=True, frozen=False)
class Data:
    id: DataId
    values: list[KeyValue]

    def add(self, value: KeyValue) -> None:
        pass
