from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Index, Integer, UniqueConstraint, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from authority.domain.model.user import User, Token
from common.port.adapter.persistence.repository.mysql import DataBase, EnumType


TokenTypeField = Enum("Token.Type", " ".join([e.name for e in Token.Type]))


class TokensTableRow(DataBase):
    __tablename__ = "tokens"
    __table_args__ = (
        (UniqueConstraint("value", name=f"uix_{__tablename__}_1")),
        (Index(f"idx_{__tablename__}_1", 'value')),
        (Index(f"idx_{__tablename__}_2", 'user_id')),
        (Index(f"idx_{__tablename__}_3", 'user_id', 'type')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    type: Mapped[int] = mapped_column(
        EnumType(enum_class=TokenTypeField),
        nullable=False,
        comment=', '.join([f'{i + 1}={e.name}' for i, e in enumerate(TokenTypeField)])
    )
    value: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True, comment="発行されたトークンの文字列")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="トークン失効日時")

    user = relationship("UsersTableRow", back_populates="tokens")

    @staticmethod
    def create(user: User) -> list[TokensTableRow]:
        return [TokensTableRow(user_id=user.id.value,
                               type=TokenTypeField[token.type.name],
                               value=token.value,
                               expires_at=token.expires_at) for token in user.tokens if not token.has_expired()]

    def to_value(self) -> Token:
        return Token(Token.Type[self.type.name], self.value, self.expires_at)
