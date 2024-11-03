from typing import Any, Dict

from pydantic import BaseModel, Field, RootModel


class DataJson(RootModel[Dict[str, Any]]):
    """データセットの1リソースに相当するレスポンスクラス"""
    pass


class JobJson(BaseModel):
    """求人情報"""
    pass


class ProfileJson(BaseModel):
    """プロフィール / 候補者情報"""
    pass
