from __future__ import annotations

from injector import singleton, inject

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user.account import Account
from authority.domain.model.user import User, UserId
from authority.port.adapter.persistence.repository.mysql.user import DriverManagerUser


@singleton
class CacheLayerUser:
    """キャッシュを保持するクラス"""
    values = dict()

    # 60秒 × 15分
    __TTL = 60 * 15

    @inject
    def __init__(self, driver_manager_user: DriverManagerUser):
        self.__driver_manager_user = driver_manager_user

    def cache_or_origin(self, user_id: UserId) -> User | None:
        key = f'id-{user_id.value}'
        if key in self.values.keys():
            return self.values[key]

        optional = self.__driver_manager_user.find_by_id(user_id)
        self.values[key] = optional
        return self.values[key]

    def caches_or_origins(self, *user_id: UserId) -> set[User] | None:
        return self.__driver_manager_user.find_by_ids(*user_id)

    def cache_or_origin_with_email_address(self, email_address: EmailAddress) -> User | None:
        key = f'email_address-{email_address.text}'
        if key in self.values.keys():
            return self.values[key]

        optional = self.__driver_manager_user.find_by_email_address(email_address)
        self.values[key] = optional
        return self.values[key]

    def cache_or_origin_with_account(self, provider: Account.Provider, provider_account_id: str) -> User | None:
        return self.__driver_manager_user.find_by_account(provider, provider_account_id)

    def cache_or_origin_with_token(self, token: str) -> User | None:
        return self.__driver_manager_user.find_by_token(token)

    def set(self, user: User) -> None:
        self.__driver_manager_user.upsert(user)
        # キャッシュを更新する
        self.values[f'email_address-{user.email_address.text}'] = user

    def delete(self, user: User) -> None:
        self.__driver_manager_user.delete(user)
        # キャッシュを更新する
        self.values[f'email_address-{user.email_address.text}'] = None
