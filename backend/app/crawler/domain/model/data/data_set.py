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

    @staticmethod
    def concat(dataset_list: list[DataSet]) -> DataSet:
        keys = set()
        for dataset in dataset_list:
            for key in dataset.to_dict().keys():
                keys.add(key)

        values = dict()
        for key in keys:
            for dataset in dataset_list:
                value: Any = dataset.to_dict().get(key, None)
                if value is not None:
                    values.update({key: value})

        return DataSet.from_dict(values)

    def to_dict(self) -> dict[str, Any]:
        return {data.name(): data.value() for data in self._set if data is not None}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> DataSet:
        return DataSet(set(Data(key, value) for key, value in data.items()))
