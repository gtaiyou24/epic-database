from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, func, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from authority.domain.model.mail import EmailAddress
from authority.domain.model.user import User, UserId
from authority.port.adapter.persistence.repository.mysql.user.driver import TokensTableRow, AccountsTableRow
from common.port.adapter.persistence.repository.mysql import DataBase


class UsersTableRow(DataBase):
    __tablename__ = "users"
    __table_args__ = ({"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"})

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False, comment="ユーザー名")
    email_address: Mapped[str] = mapped_column(String(255),
                                               unique=True,
                                               nullable=False,
                                               index=True,
                                               comment='メールアドレス')
    password: Mapped[str | None] = mapped_column(String(255),
                                                 nullable=True,
                                                 comment='セキュアなパスワード。OAuth2 でサービス登録している場合は NULL になる。')
    enable: Mapped[bool] = mapped_column(Boolean,
                                         default=False,
                                         nullable=False,
                                         comment='有効化されているかどうか')
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),
                                                         nullable=True,
                                                         comment='本人確認が完了した日時')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    tokens: Mapped[list[TokensTableRow]] = relationship(back_populates="user", lazy='joined')
    accounts: Mapped[list[AccountsTableRow]] = relationship(back_populates="user", lazy='joined')

    @staticmethod
    def create(user: User) -> UsersTableRow:
        return UsersTableRow(
            id=user.id.value,
            username=user.username,
            email_address=user.email_address.text,
            password=user.encrypted_password,
            enable=user.enable,
            verified_at=user.verified_at,
            tokens=[tr for tr in TokensTableRow.create(user)],
            accounts=[tr for tr in AccountsTableRow.create(user)]
        )

    def update(self, user: User) -> None:
        self.username = user.username
        self.email_address = user.email_address.text
        self.password = user.encrypted_password
        self.enable = user.enable
        self.verified_at = user.verified_at
        self.tokens = TokensTableRow.create(user)
        self.accounts = AccountsTableRow.create(user)

    def to_entity(self) -> User:
        return User(
            id=UserId(self.id),
            username=self.username,
            email_address=EmailAddress(self.email_address),
            encrypted_password=self.password,
            tokens=set([tr.to_value() for tr in self.tokens]),
            accounts=set([tr.to_value() for tr in self.accounts]),
            verified_at=self.verified_at,
            enable=self.enable
        )
