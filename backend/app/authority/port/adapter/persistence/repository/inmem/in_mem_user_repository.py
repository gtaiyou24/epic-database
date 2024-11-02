from __future__ import annotations

import uuid
from typing import override

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user import UserRepository, User, UserId
from authority.domain.model.user.account import Account


class InMemUserRepository(UserRepository):
    def __init__(self):
        self.users: set[User] = set()

    @override
    def next_identity(self) -> UserId:
        return UserId(str(uuid.uuid4()))

    @override
    def add(self, user: User) -> None:
        self.users.add(user)

    @override
    def remove(self, user: User) -> None:
        self.users.remove(user)

    @override
    def get(self, *user_id: UserId) -> User | list[User] | None:
        if len(user_id) == 1:
            for user in self.users:
                if user.id in user_id:
                    return user
            return None

        user_list = []
        for user in self.users:
            if user.id in user_id:
                user_list.append(user)
        return user_list

    @override
    def user_with_token(self, value: str) -> User | None:
        for user in self.users:
            if user.token_with(value):
                return user
        return None

    @override
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        for user in self.users:
            if user.email_address == email_address:
                return user
        return None

    @override
    def users_with_ids(self, *user_id: UserId) -> list[User]:
        users = list()
        for u in self.users:
            if u.id in user_id:
                users.append(u)
        return users

    @override
    def user_with_account(self, provider: Account.Provider, provider_account_id: str) -> User | None:
        for u in self.users:
            if u.is_assigned_to(provider) and provider_account_id in [a.provider_account_id for a in u.accounts]:
                return u
        return None
