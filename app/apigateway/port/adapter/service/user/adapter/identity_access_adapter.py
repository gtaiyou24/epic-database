import abc

from apigateway.domain.model.user import User


class IdentityAccessAdapter(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, access_token: str) -> User:
        pass
