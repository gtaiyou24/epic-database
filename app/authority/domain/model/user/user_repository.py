from __future__ import annotations

import abc

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user import User, UserId
from authority.domain.model.user.account import Account


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> UserId:
        pass

    @abc.abstractmethod
    def add(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def remove(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def get(self, user_id: UserId) -> User | None:
        pass

    @abc.abstractmethod
    def user_with_token(self, value: str) -> User | None:
        pass

    @abc.abstractmethod
    def users_with_ids(self, *user_id: UserId) -> set[User]:
        pass

    @abc.abstractmethod
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        pass

    @abc.abstractmethod
    def user_with_account(self, provider: Account.Provider, provider_account_id: str) -> User | None:
        pass
