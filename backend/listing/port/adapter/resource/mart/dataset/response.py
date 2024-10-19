from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field, RootModel


class DataJson(RootModel[Dict[str, Any]]):
    """データセットの1リソースに相当するレスポンスクラス"""
    pass


class CompanyJson(BaseModel):
    """企業情報"""
    class ContactPoint(BaseModel):
        contact_type: str | None = Field(title="問合せ用途", examples=["カスタマーサポート"])

    class Telephone(ContactPoint):
        telephone: str = Field(title="電話番号")

    class Email(ContactPoint):
        email: str = Field(title="電話番号")

    class FaxNumber(ContactPoint):
        fax_number: str = Field(title="FAX番号")

    class URL(ContactPoint):
        url: str = Field(title="お問合せURL")

    class Address(BaseModel):
        country: str = Field(title="国名", examples=["JP"])
        postal_code: int = Field(title="郵便番号", min_length=7, max_length=7, examples=[1028282])
        prefecture: str = Field(title="都道府県", examples=["東京都"])
        city: str = Field(title="市区町村", examples=["千代田区"])
        street: str = Field(title="番地/建物", examples=["紀尾井町1-3 東京ガーデンテラス紀尾井町 紀尾井タワー"])

    name: str = Field(title="企業名", examples=["LINEヤフー株式会社"])
    description: str = Field(title="企業の概略", examples=["インターネット広告事業、イーコマース事業及び会員サービス事業などの展開並びにグループ会社の経営管理業務など"])
    url: str = Field(title="コーポレートサイト", examples=["https://www.lycorp.co.jp"])
    representative: list[str] = Field(title="代表者", examples=["川邊健太郎", "出澤剛"])
    founded_at: datetime = Field(title="設立日", examples=["1996-01-31"])
    fiscal_year_end: int = Field(title="決算月", examples=[3])
    capital: int = Field(title="資本金", examples=[248144000000])
    sales: int = Field(title="売上高", examples=[1814663000000])
    employees: int = Field(title="従業員数", examples=[1000])
    telephone: str = Field(title="電話番号")
    fax_number: str = Field(title="FAX番号")
    contact_points: list[ContactPoint] = Field(title="問合せ情報", default=[])
    offices: list[Address] = Field(title="事業所/オフィス", default=[])
    same_as: list[str] = Field(title="関連サイトやSNS", default=[])

    # 子会社(subsidiaries)
    # 業界(大業界・小業界)
    # 事業内容
    # 上場区分
    # 信用情報
    # 成長率(成長率/従業員増減率)
    # 人
    # ニュース
    # 採用


class JobJson(BaseModel):
    """求人情報"""
    pass


class ProfileJson(BaseModel):
    """プロフィール / 候補者情報"""
    pass
