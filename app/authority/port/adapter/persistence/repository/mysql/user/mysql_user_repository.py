from __future__ import annotations

import uuid

from injector import inject
from typing import override

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user.account import Account
from authority.domain.model.user import UserRepository, User, UserId
from authority.port.adapter.persistence.repository.mysql.user import CacheLayerUser


class MySQLUserRepository(UserRepository):

    @inject
    def __init__(self, cache_layer_user: CacheLayerUser):
        self.__cache_layer_user = cache_layer_user

    @override
    def next_identity(self) -> UserId:
        return UserId(str(uuid.uuid4()))

    @override
    def add(self, user: User) -> None:
        self.__cache_layer_user.set(user)

    @override
    def remove(self, user: User) -> None:
        self.__cache_layer_user.delete(user)

    @override
    def get(self, user_id: UserId) -> User | None:
        return self.__cache_layer_user.cache_or_origin(user_id)

    @override
    def user_with_token(self, value: str) -> User | None:
        return self.__cache_layer_user.cache_or_origin_with_token(value)

    @override
    def users_with_ids(self, *user_id: UserId) -> set[User]:
        return self.__cache_layer_user.caches_or_origins(*user_id)

    @override
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        return self.__cache_layer_user.cache_or_origin_with_email_address(email_address)

    @override
    def user_with_account(self, provider: Account.Provider, provider_account_id: str) -> User | None:
        return self.__cache_layer_user.cache_or_origin_with_account(provider, provider_account_id)
