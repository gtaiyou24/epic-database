import abc

from apigateway.domain.model.secret import Secret, Key


class SecretManagerService(abc.ABC):
    @abc.abstractmethod
    def get(self, key: Key, version: float | None = None) -> Secret:
        pass
