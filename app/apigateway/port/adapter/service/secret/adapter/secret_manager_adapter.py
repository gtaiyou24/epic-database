import abc

from apigateway.domain.model.secret import Key, Secret


class SecretManagerAdapter(abc.ABC):
    @abc.abstractmethod
    def get(self, key: Key, version: float) -> Secret:
        pass
