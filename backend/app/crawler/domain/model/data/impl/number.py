from __future__ import annotations

from dataclasses import dataclass
from numbers import Number

from crawler.domain.model.data import Data


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Number(Data):
    _name: str
    _value: float | int

    def __init__(self, name: str, value: float | int):
        super().__setattr__("_name", name)
        super().__setattr__("_value", value)

    @staticmethod
    def new(value: tuple[str, float | int]) -> Number:
        name = value[0]
        value = value[1]
        return Number(name, value)

    def name(self) -> str:
        return self._name

    def value(self) -> float | int:
        return self._value
