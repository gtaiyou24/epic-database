from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from apigateway.domain.model.user import UserId, EmailAddress


@dataclass(init=False, unsafe_hash=True, frozen=True)
class User:
    id: UserId
    username: str
    email_address: EmailAddress
    enable: bool
    accounts: set[Account]
    verified_at: datetime | None

    def __init__(self,
                 id: UserId,
                 username: str,
                 email_address: EmailAddress,
                 enable: bool,
                 accounts: set[Account],
                 verified_at: datetime | None = None) -> None:
        assert id, "ユーザーIDは必須です。"
        assert username, "ユーザー名は必須です。"
        assert email_address, "メールアドレスは必須です。"
        assert isinstance(enable, bool), f"enable プロパティには {type(enable)} 型ではなく bool 型を指定してください。"
        super().__setattr__("id", id)
        super().__setattr__("username", username)
        super().__setattr__("email_address", email_address)
        super().__setattr__("enable", enable)
        super().__setattr__("accounts", accounts)
        super().__setattr__("verified_at", verified_at)


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Account:
    provider: Literal['GOOGLE', 'FACEBOOK', 'LINE', 'X', 'LINKEDIN', 'SLACK', 'WANTEDLY']
    provider_account_id: str
    tokens: Tokens
    scope: str
    id_token: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Tokens:
    access_token: str
    refresh_token: str | None
    expires_at: datetime
    token_type: Literal['BEARER']