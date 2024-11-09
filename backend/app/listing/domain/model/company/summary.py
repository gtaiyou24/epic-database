from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass(init=True, frozen=True)
class Summary:
    """企業情報のサマリー

    比較的に情報の更新頻度が多い情報をまとめた値オブジェクト
    """
    class Name(Enum):
        REPRESENTATIVE = 'representative'  # 代表者
        FISCAL_YEAR_END = 'fiscal_year_end'  # 決算月
        CAPITAL = 'capital'  # 資本金
        SALES = 'sales'  # 売上高
        EMPLOYEES = 'employees'  # 従業員数
        # 子会社(subsidiaries)
        # 業界(大業界・小業界)
        # 上場区分
        # 信用情報
        # 倒産確率
        # 成長率(成長率/従業員増減率)

        @staticmethod
        def value_of(value: str) -> Summary.Name:
            for name in Summary.Name:
                if name.value == value:
                    return name
            raise ValueError(f"Summary.Name '{value}' is not found")

        def make(self, value: Any) -> Summary:
            return Summary(self, value)

    name: Name
    value: Any

    def __hash__(self):
        return hash(self.name.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Summary):
            return False
        return self.name.value == other.name.value and self.value == other.value


class Representative(Summary):
    value: list[str]  # ["川邊健太郎", "出澤剛"]
