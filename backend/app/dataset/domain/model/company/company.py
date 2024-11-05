from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from dataset.domain.model.company import CompanyId, ContactPoint, Summary, Address
from dataset.domain.model.url import URL


@dataclass(init=False, eq=False)
class Company:
    id: CompanyId
    name: str
    description: str
    # TODO: 業界(大業界・小業界)
    founded_at: date
    homepage: URL  # ホームページURL
    same_as: list[URL]  # 関連サイトやSNS
    summaries: set[Summary]  # その他企業情報
    contact_points: set[ContactPoint]  # 企業への問い合わせ情報
    offices: set[Address]  # 事業所 / オフィス
    # employees: set[Employee]  # 従業員一覧
    # news: list[NewsId]  # ニュース一覧
    # job: set[JobId]  # 採用一覧

    def __init__(self,
                 id: CompanyId,
                 name: str,
                 description: str,
                 founded_at: date,
                 homepage: URL,
                 same_as: list[URL],
                 summaries: set[Summary] = {},
                 contact_points: set[ContactPoint] = {},
                 offices: set[Address] = {}):
        super().__setattr__("id", id)
        super().__setattr__("name", name)
        super().__setattr__("description", description)
        super().__setattr__("founded_at", founded_at)
        super().__setattr__("homepage", homepage)
        super().__setattr__("same_as", same_as)
        super().__setattr__("summaries", summaries)
        super().__setattr__("contact_points", contact_points)
        super().__setattr__("offices", offices)

    def __eq__(self, other: Company) -> bool:
        if not isinstance(other, Company):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
