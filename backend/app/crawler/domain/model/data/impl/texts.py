from __future__ import annotations

from dataclasses import dataclass

from crawler.domain.model.data import Data


@dataclass(init=False, frozen=True)
class Texts(Data):
    _name: str
    values: list[str] | set[str]

    def __init__(self, name: str, values: list[str] | set[str]):
        super().__setattr__("_name", name)
        super().__setattr__("values", values)

    @staticmethod
    def new(value: tuple[str, list[str] | set[str]]) -> Texts:
        name = value[0]
        values = value[1]
        return Texts(name, values)

    def name(self) -> str:
        return self._name

    def value(self) -> list[str] | set[str]:
        return self.values

    def __hash__(self):
        return hash(
            self._name + "-" + str(sorted([value for value in self.values]))
        )

    def __eq__(self, other):
        if not isinstance(other, Texts):
            return False
        return self.__hash__() == other.__hash__()
