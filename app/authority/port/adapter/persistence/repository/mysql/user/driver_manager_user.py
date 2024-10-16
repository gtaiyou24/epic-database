from __future__ import annotations

from injector import inject

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user.account import Account
from authority.domain.model.user import User, UserId
from authority.port.adapter.persistence.repository.mysql.user.driver import UsersTableRow, TokensTableRow, AccountsTableRow
from common.application import UnitOfWork
from common.port.adapter.persistence.repository.mysql import MySQLUnitOfWork


class DriverManagerUser:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_by_id(self, user_id: UserId) -> User | None:
        with self.__unit_of_work.query() as q:
            optional: UsersTableRow | None = q.query(UsersTableRow).get(user_id.value)
            if optional is None:
                return None
            return optional.to_entity()

    def find_by_ids(self, *user_id: UserId) -> set[User]:
        with self.__unit_of_work.query() as q:
            table_rows: list[UsersTableRow] = q.query(UsersTableRow)\
                .filter(UsersTableRow.id.in_([_id.value for _id in user_id]))
            return set([tr.to_entity() for tr in table_rows])

    def find_one_by(self, **kwargs) -> User | None:
        with self.__unit_of_work.query() as q:
            optional: UsersTableRow | None = q.query(UsersTableRow).filter_by(**kwargs).one_or_none()
            if optional is None:
                return None
            return optional.to_entity()

    def find_all_by(self, **kwargs) -> list[User]:
        with self.__unit_of_work.query() as q:
            return [e.to_entity() for e in q.query(UsersTableRow).filter_by(**kwargs).all()]

    def find_by_email_address(self, email_address: EmailAddress) -> User | None:
        with self.__unit_of_work.query() as q:
            optional: UsersTableRow | None = q.query(UsersTableRow)\
                .filter_by(email_address=email_address.text, deleted=False)\
                .one_or_none()
            return optional.to_entity() if optional else None

    def find_by_account(self, provider: Account.Provider, provider_account_id: str) -> User | None:
        with self.__unit_of_work.query() as q:
            optional: AccountsTableRow | None = q.query(AccountsTableRow)\
                .filter_by(provider=provider.name, provider_account_id=provider_account_id)\
                .one_or_none()
            return optional.user.to_entity() if optional else None

    def find_by_token(self, value: str) -> User | None:
        with self.__unit_of_work.query() as q:
            optional: TokensTableRow | None = q.query(TokensTableRow).filter_by(value=value).one_or_none()
            return optional.user.to_entity() if optional else None

    def upsert(self, user: User) -> None:
        exists = self.__unit_of_work.session().query(UsersTableRow).filter_by(id=user.id.value).exists()
        if self.__unit_of_work.session().query(exists).scalar():
            self.update(user)
        else:
            self.insert(user)

    def insert(self, user: User) -> None:
        self.__unit_of_work.persist(UsersTableRow.create(user))

    def update(self, user: User) -> None:
        optional: UsersTableRow | None = self.__unit_of_work.session().query(UsersTableRow).get(user.id.value)
        if optional is None:
            raise Exception(f'{UsersTableRow.__tablename__}.{user.id.value} が存在しないため、更新できません。')

        self.__unit_of_work.delete(*optional.tokens)
        self.__unit_of_work.delete(*optional.accounts)
        self.__unit_of_work.flush()

        optional.update(user)

    def delete(self, user: User) -> None:
        optional: UsersTableRow | None = self.__unit_of_work.session().query(UsersTableRow).get(user.id.value)
        if optional is None:
            return None

        self.__unit_of_work.delete(*optional.tokens)
        self.__unit_of_work.delete(*optional.accounts)
        self.__unit_of_work.flush()

        self.__unit_of_work.delete(optional)
