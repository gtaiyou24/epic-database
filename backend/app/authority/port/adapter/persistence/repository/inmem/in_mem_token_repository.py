from typing import override

from apigateway.domain.model.token import BearerToken
from authority.domain.model.token import TokenRepository


class InMemTokenRepository(TokenRepository):
    def __init__(self):
        self.tokens = set()

    @override
    def add(self, token: BearerToken) -> None:
        self.tokens.add(token)

    @override
    def remove(self, *token: BearerToken) -> None:
        self.tokens.remove(*token)

    @override
    def token_with_value(self, value: str) -> BearerToken | None:
        for token in self.tokens:
            if token.address == value:
                return token
