from typing import Literal

from pydantic import BaseModel, Field

type Provider = Literal['GOOGLE']


class LinkAccountRequest(BaseModel):
    provider: Provider = Field(title="連携するプロバイダー名")
    code: str = Field(title='認証コード')
    redirect_uri: str = Field(title='リダイレクトURI')
    code_verifier: str | None = Field(title='コード検証'),
    grant_type: str = Field(title='タイプ')


class UnlinkAccountRequest(BaseModel):
    provider: Provider = Field(title="連携解除するプロバイダー名")
