from __future__ import annotations

from dataclasses import dataclass

from crawler.domain.model.data import Data


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Boolean(Data):
    _name: str
    true_or_false: bool

    def __init__(self, name: str, value: bool):
        super().__setattr__("_name", name)
        super().__setattr__("true_or_false", value)

    @staticmethod
    def new(value: tuple[str, bool]) -> Boolean:
        name = value[0]
        value = value[1]
        return Boolean(name, value)

    def name(self) -> str:
        return self._name

    def value(self) -> bool:
        return self.true_or_false
