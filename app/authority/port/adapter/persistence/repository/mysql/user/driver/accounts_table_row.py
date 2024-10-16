from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, TEXT, DateTime, String, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from authority.domain.model.user import User
from authority.domain.model.user.account import Account, ProviderTokens
from common.port.adapter.persistence.repository.mysql import DataBase


class AccountsTableRow(DataBase):
    __tablename__ = "accounts"
    __table_args__ = (
        (UniqueConstraint("user_id", "provider", "provider_account_id", name=f"uix_{__tablename__}_1")),
        (Index(f"idx_{__tablename__}_1", 'provider', 'provider_account_id')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    provider: Mapped[str] = mapped_column(String(255), nullable=False, comment="プロバイダー名")
    provider_account_id: Mapped[str] = mapped_column(String(255), nullable=False, comment="プロバイダーで発行されたアカウントID")
    access_token: Mapped[str | None] = mapped_column(TEXT, nullable=True, comment="プロバイダーが発行したアクセストークン")
    refresh_token: Mapped[str | None] = mapped_column(TEXT, nullable=True, comment="プロバイダーが発行したリフレッシュトークン")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="トークン失効日時")
    token_type: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    scope: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    id_token: Mapped[str | None] = mapped_column(TEXT, nullable=True)

    user = relationship("UsersTableRow", back_populates="accounts", lazy='joined')

    @staticmethod
    def create(user: User) -> list[AccountsTableRow]:
        return [AccountsTableRow(user_id=user.id.value,
                                 provider=account.provider.name,
                                 provider_account_id=account.provider_account_id,
                                 access_token=account.tokens.access_token,
                                 refresh_token=account.tokens.refresh_token,
                                 expires_at=account.tokens.expires_at,
                                 token_type=account.tokens.token_type.name,
                                 scope=account.scope,
                                 id_token=account.id_token) for account in user.accounts]

    def to_value(self) -> Account:
        return Account.Provider[self.provider].make(
            provider_account_id=self.provider_account_id,
            tokens=ProviderTokens(
                access_token=self.access_token,
                refresh_token=self.refresh_token,
                expires_at=self.expires_at,
                token_type=ProviderTokens.TokenType[self.token_type]
            ),
            scope=self.scope,
            id_token=self.id_token
        )
