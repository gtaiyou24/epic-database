from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from listing.application.company.dpo import CompanyDpo
from listing.domain.model.company import CompanyId, ContactPoint


class CompanyJson(BaseModel):
    """企業情報"""
    class ContactPoint(BaseModel):
        @staticmethod
        def from_(contact_point: ContactPoint) -> CompanyJson.ContactPoint:
            if contact_point.type == ContactPoint.Type.TELEPHONE:
                return CompanyJson.Telephone(telephone=contact_point.value)
            elif contact_point.type == ContactPoint.Type.EMAIL:
                return CompanyJson.Email(email=contact_point.value)
            elif contact_point.type == ContactPoint.Type.FAX:
                return CompanyJson.FaxNumber(fax_number=contact_point.value)
            else:
                raise ValueError(f"意図しないお問い合わせ情報 {contact_point.type.value} を返却しようとしています")

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
        postal_code: str | None = Field(title="郵便番号", default=None, examples=['1028282'])
        prefecture: str = Field(title="都道府県", examples=["東京都"])
        city: str = Field(title="市区町村", examples=["千代田区"])
        street: str = Field(title="番地/建物", examples=["紀尾井町1-3 東京ガーデンテラス紀尾井町 紀尾井タワー"])

    uuid: str | None = Field(title="UUID", description="EpicDataBaseが発行した企業ID", default=None)
    jcn: str = Field(title="法人番号", description="日本の法人番号(Japan Corporate Number)")
    name: str = Field(title="企業名", examples=["LINEヤフー株式会社"])
    description: str | None = Field(title="企業の概略", default=None,
                                    examples=["インターネット広告事業、イーコマース事業及び会員サービス事業などの展開並びにグループ会社の経営管理業務など"])
    founded_at: datetime | None = Field(title="設立日", default=None, examples=["1996-01-31"])
    homepage: str | None = Field(title="コーポレートサイト", default=None, examples=["https://www.lycorp.co.jp"])
    same_as: list[str] = Field(title="関連サイトやSNS", examples=[['https://www.lycorp.co.jp/ja/']], default=[])
    summaries: dict[str, Any] = Field(title="企業詳細情報一覧", default=[], examples=[{
        "representative": ["川邊健太郎", "出澤剛"],
        "fiscal_year_end": 3,
        "capital": 248144000000,
        "sales": "1814663000000",
        "employees": 11176
    }])
    contact_points: list[ContactPoint] = Field(
        title="問合せ情報",
        examples=[[
            URL(url='https://www.lycorp.co.jp/ja/contact/'),
            Telephone(telephone='03-6779-4900')
        ]],
        default=[]
    )
    offices: list[Address] = Field(
        title="事業所/オフィス",
        examples=[[
            Address(country='JP', postal_code='1028282', prefecture='東京都', city='千代田区',
                    street='紀尾井町1-3 東京ガーデンテラス紀尾井町 紀尾井タワー'),
        ]],
        default=[]
    )

    @staticmethod
    def from_(dpo: CompanyDpo) -> CompanyJson:
        return CompanyJson(
            uuid=dpo.company.id.type_of(CompanyId.Type.UUID).value,
            jcn=dpo.company.id.type_of(CompanyId.Type.JCN).value,
            name=dpo.company.name,
            description=dpo.company.description,
            founded_at=dpo.company.founded_at,
            homepage=dpo.company.homepage.address if dpo.company.homepage else None,
            same_as=[url.address for url in dpo.company.same_as],
            summaries={summary.name.value: summary.value for summary in dpo.company.summaries},
            contact_points=[
                CompanyJson.ContactPoint.from_(contact_point) for contact_point in dpo.company.contact_points
            ],
            offices=[CompanyJson.Address(
                country=office.country,
                postal_code=office.postal_code,
                prefecture=office.prefecture.ja,
                city=office.city,
                street=office.street
            ) for office in dpo.company.offices],
        )
