from typing import override

from injector import inject

from apigateway.domain.model.user import IdentityAccessService, User
from apigateway.port.adapter.service.user.adapter import IdentityAccessAdapter


class IdentityAccessServiceImpl(IdentityAccessService):
    @inject
    def __init__(self, identity_access_adapter: IdentityAccessAdapter):
        self.__identity_access_adapter = identity_access_adapter

    @override
    def authenticate(self, access_token: str) -> User:
        return self.__identity_access_adapter.authenticate(access_token)
