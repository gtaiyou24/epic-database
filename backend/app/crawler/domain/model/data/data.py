from __future__ import annotations

import abc
from typing import Any


class Data(abc.ABC):
    @staticmethod
    def new(value: Any) -> Data:
        """データを生成します。"""
        raise NotImplementedError()

    @abc.abstractmethod
    def name(self) -> str:
        """データ名を返す。"""

    @abc.abstractmethod
    def value(self) -> Any:
        """データの値を返す。"""
