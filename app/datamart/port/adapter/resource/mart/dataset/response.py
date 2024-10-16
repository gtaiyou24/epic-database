import abc
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DataJson(abc.ABC, BaseModel):
    id: str = Field(title="データID")
    payload: dict[str, Any] | list[dict[str, Any]] = Field(title="ペイロード", description="ユーザーが設定した加工データを提供")


class CorporationJson(DataJson):
    """企業情報"""
    class ContactPoint(BaseModel):
        telephone: str = Field(title="電話番号")
        contact_type: str = Field(title="問合せ用途", examples=["カスタマーサポート"])

    class Location(BaseModel):
        pass

    name: str = Field(title="企業名")
    founder: list[str] = Field(title="創業者")
    founded_at: datetime = Field(title="設立日")
    description: str = Field(title="企業の概略")
    telephone: str = Field(title="電話番号")
    fax_number: str = Field(title="FAX番号")
    contact_points: list[ContactPoint] = Field(title="問合せ情報", default=[])
    locations: list[Location] = Field(title="事業所/オフィス", default=[])
    urls: list[str] = Field(title="関連サイトやSNS", default=[])


class JobJson(DataJson):
    """求人情報"""
    pass


class ProfileJson(DataJson):
    """プロフィール / 候補者情報"""
    pass
