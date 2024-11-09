from __future__ import annotations

from typing import Any


class Data:
    def __init__(self, name: str, value: Any):
        self.__name = name
        if isinstance(value, str):
            value = value.replace('\n', '').strip()
        self.__value = value

    @staticmethod
    def new(value: Any) -> Data:
        """データを生成します。"""
        raise NotImplementedError()

    def name(self) -> str:
        """データ名を返す。"""
        return self.__name

    def value(self) -> Any:
        """データの値を返す。"""
        return self.__value
