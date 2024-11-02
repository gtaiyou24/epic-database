import abc
from enum import Enum


class Summary(abc.ABC):
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

    name: Name
    value: str


class Representative(Summary):
    person_names: list[str]  # ["川邊健太郎", "出澤剛"]
