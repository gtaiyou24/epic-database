import abc

from apigateway.domain.model.token import BearerToken


class TokenRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, token: BearerToken) -> None:
        pass

    @abc.abstractmethod
    def remove(self, *token: BearerToken) -> None:
        pass

    @abc.abstractmethod
    def token_with_value(self, value: str) -> BearerToken | None:
        pass
