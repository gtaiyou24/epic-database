from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from crawler.domain.model.data import Data


@dataclass(init=False, unsafe_hash=True, frozen=True)
class DataSet:
    _set: set[Data]

    def __init__(self, dataset: set[Data]):
        assert isinstance(dataset, set), "DataSetのコンストラクにはSet型を指定してください。"
        super().__setattr__("_set", {data for data in dataset if data is not None})

    def add(self, data: Data) -> DataSet:
        data_list = {data for data in self._set}
        data_list.add(data)
        return DataSet(data_list)

    def to_dict(self) -> dict[str, Any]:
        return {data.name(): data.value() for data in self._set if data is not None}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> DataSet:
        return DataSet(set())
