from __future__ import annotations

import abc
import datetime
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Literal, Callable

import pytz

from apigateway.domain.model.user import UserId
from common.exception import SystemException, ErrorCode

type TokenType = Literal[*[e.name for e in BearerToken.Type]]


@dataclass(init=True, unsafe_hash=False, frozen=True)
class BearerToken(abc.ABC):
    """Bearerトークン

    仕様については、RFCを参照してください。
    * https://tex2e.github.io/rfc-translater/html/rfc6749.html
    * https://tex2e.github.io/rfc-translater/html/rfc7009.html
    """
    class Type(Enum):
        ACCESS = ("access_token", lambda user_id, value, published_at, expires_at, pair_token: AccessToken(
            user_id, value, published_at, expires_at, pair_token))
        REFRESH = ("refresh_token", lambda user_id, value, published_at, expires_at, pair_token: RefreshToken(
            user_id, value, published_at, expires_at, pair_token))

        def __init__(self,
                     key: str,
                     make: Callable[[UserId, str, datetime.datetime, datetime.datetime, str], BearerToken]):
            self.__key = key
            self.__make = make

        def make(self,
                 user_id: UserId,
                 value: str,
                 published_at: datetime.datetime,
                 expires_at: datetime.datetime,
                 pair_token: str) -> BearerToken:
            return self.__make(user_id, value, published_at, expires_at, pair_token)

    type: Type
    user_id: UserId
    value: str
    published_at: datetime.datetime
    expires_at: datetime.datetime
    pair_token: str

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: BearerToken):
        if not isinstance(other, BearerToken):
            return False
        return self.value == other.value

    def type_is(self, type: TokenType) -> bool:
        return self.type == type

    def is_expired(self) -> bool:
        tz = pytz.timezone('Asia/Tokyo')
        return self.expires_at.astimezone(tz) < datetime.datetime.now().astimezone(tz)

    def is_published_after(self, published_at: datetime.datetime) -> bool:
        tz = pytz.timezone('Asia/Tokyo')
        return self.published_at.astimezone(tz) > published_at.astimezone(tz)


class AccessToken(BearerToken):
    """アクセストークン

    RFC
    * https://tex2e.github.io/rfc-translater/html/rfc6749.html#1-4--Access-Token
    """

    def __init__(self,
                 user_id: UserId,
                 value: str,
                 published_at: datetime.datetime,
                 expires_at: datetime.datetime,
                 pair_token: str):
        super().__init__(BearerToken.Type.ACCESS, user_id, value, published_at, expires_at, pair_token)

    @staticmethod
    def generate(user_id: UserId) -> (AccessToken, RefreshToken):
        """アクセストークンを発行する

        リフレッシュトークンは、RFC 6749 の説明からアクセストークンが発行されるタイミングで一緒に発行させるため、
        アクセストークンの生成ロジック内でリフレッシュトークンも生成しています。
        """
        tz = pytz.timezone('Asia/Tokyo')
        published_at = datetime.datetime.now().astimezone(tz)

        access_token_value = str(uuid.uuid4())
        refresh_token_value = str(uuid.uuid4())

        return (
            AccessToken(
                user_id,
                access_token_value,
                published_at,
                published_at + datetime.timedelta(seconds=60 * 60),
                refresh_token_value
            ),
            RefreshToken(
                user_id,
                refresh_token_value,
                published_at,
                published_at + datetime.timedelta(seconds=60 * 60 * 24 * 30),
                access_token_value
            )
        )


class RefreshToken(BearerToken):
    """リフレッシュトークン

    https://tex2e.github.io/rfc-translater/html/rfc6749.html#1-5--Refresh-Token

    RFC 6749 の Refresh Token の節によると、リフレッシュトークンは、アクセストークンを発行するときに一緒に発行されるます。
    ただし、リフレッシュトークンの発行は任意であり、必ずリフレッシュトークンを発行しなくとも良い。

    リフレッシュトークンは、認可サーバー(この場合、API Gateway)でアクセストークンを再発行することのみを目的としており、
    リソースサーバー(ex. 商品やユーザー、注文API)に送信されることはありません。
    """

    def __init__(self,
                 user_id: UserId,
                 value: str,
                 published_at: datetime.datetime,
                 expires_at: datetime.datetime,
                 pair_token: str):
        super().__init__(BearerToken.Type.REFRESH, user_id, value, published_at, expires_at, pair_token)

    def refresh(self) -> (AccessToken, RefreshToken):
        """新しくアクセストークンを発行する"""
        if self.is_expired():
            raise SystemException(ErrorCode.INVALID_TOKEN, f"リフレッシュトークン {self.value} は無効です。")
        return AccessToken.generate(self.user_id)
