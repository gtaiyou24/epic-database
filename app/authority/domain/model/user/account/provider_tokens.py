from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import Enum


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ProviderTokens:
    """アカウントプロバイダーが発行したトークン"""
    class TokenType(Enum):
        BEARER = 'bearer'

        @staticmethod
        def value_of(value: str) -> ProviderTokens.TokenType:
            for e in ProviderTokens.TokenType:
                if e.value == value:
                    return e
            raise ValueError(f"TokenType {value} is not found")

    access_token: str
    refresh_token: str | None
    expires_at: datetime.datetime
    token_type: TokenType
