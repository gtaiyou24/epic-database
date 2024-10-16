from __future__ import annotations

from dataclasses import dataclass

import jwt

from apigateway.domain.model.secret import Secret
from apigateway.domain.model.token.internal import InternalToken



@dataclass(init=True, unsafe_hash=True, frozen=True)
class InternalTokenDpo:
    __internal_token: InternalToken
    __secret: Secret

    def add_audience(self, url: str) -> InternalTokenDpo:
        internal_token = self.__internal_token.add_audience(url)
        return InternalTokenDpo(internal_token, self.__secret)

    def generate_jwt(self) -> str:
        return jwt.encode(self.__internal_token.payload, self.__secret.value, algorithm='RS256')
