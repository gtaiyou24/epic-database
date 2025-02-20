from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, override

from crawler.domain.model.data import Data


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Text(Data):
    _name: str
    free_text: str

    def __init__(self, name: str, value: str):
        super().__setattr__("_name", name)
        super().__setattr__("free_text", value)

    @staticmethod
    @override
    def new(value: Tuple[str, str]) -> Text:
        name = value[0]
        value = value[1]
        return Text(name, value)

    @override
    def name(self) -> str:
        return self._name

    @override
    def value(self) -> str:
        return self.free_text
