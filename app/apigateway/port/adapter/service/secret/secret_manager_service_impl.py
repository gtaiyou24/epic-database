from typing import override

from injector import inject

from apigateway.domain.model.secret import SecretManagerService, Key, Secret
from apigateway.port.adapter.service.secret.adapter import SecretManagerAdapter


class SecretManagerServiceImpl(SecretManagerService):
    @inject
    def __init__(self, secret_manager_adapter: SecretManagerAdapter):
        self.__secret_manager_adapter = secret_manager_adapter

    @override
    def get(self, key: Key, version: float | None = None) -> Secret:
        return self.__secret_manager_adapter.get(key, version)
