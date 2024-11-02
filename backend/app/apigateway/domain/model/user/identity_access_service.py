import abc

from apigateway.domain.model.user import User


class IdentityAccessService(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, access_token: str) -> User:
        pass
