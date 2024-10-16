from __future__ import annotations

from pydantic import BaseModel, Field

from authority.application.authorization.dpo import TokenDpo


class TokenJson(BaseModel):
    access_token: str = Field(title="アクセストークン")
    refresh_token: str = Field(title="リフレッシュトークン")
    token_type: str = Field(title="トークンタイプ", default="bearer")
    expires_at: float = Field(title="アクセストークンの有効期間タイムスタンプ")

    @staticmethod
    def from_(dpo: TokenDpo) -> TokenJson:
        access_token = dpo.access_token
        refresh_token = dpo.refresh_token
        if access_token is None or refresh_token is None:
            raise ValueError("アクセストークン、リフレッシュトークンの生成に失敗しました")
        return TokenJson(
            access_token=access_token.value,
            refresh_token=refresh_token.value,
            token_type="bearer",
            expires_at=access_token.expires_at.timestamp(),
        )
