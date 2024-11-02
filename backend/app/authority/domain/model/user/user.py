from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from authority.domain.model.mail import EmailAddress
from authority.domain.model.token import AccessToken, RefreshToken
from authority.domain.model.user.account import Account
from authority.domain.model.user import Token, EncryptionService, UserId, VerificationTokenGenerated, \
    PasswordResetTokenGenerated
from common.domain.model import DomainRegistry, DomainEventPublisher


@dataclass(init=True, eq=False)
class User:
    id: UserId
    username: str
    email_address: EmailAddress
    encrypted_password: str | None
    tokens: set[Token]
    enable: bool
    accounts: set[Account]
    verified_at: datetime | None

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def provision(id: UserId,
                  username: str,
                  email_address: EmailAddress,
                  plain_password: str | None = None,
                  account: Account | None = None) -> User:
        """ユーザーを作成する"""
        enable = False
        accounts = set()
        verified_at = None
        if account:
            # GitHub や Google で登録した場合、account が存在します。この場合、メアド認証は不要になるので enable を True にします。
            enable = True
            accounts.add(account)
            verified_at = datetime.now()

        user = User(id, username, email_address, None, set(), enable, accounts, verified_at)

        if plain_password:
            user.protect_password(plain_password)

        if enable is False:
            # メアド検証用のトークンを発行する
            user.generate(Token.Type.VERIFICATION)

        return user

    def verify_password(self, plain_password: str) -> bool:
        if self.encrypted_password is None:
            return False
        return DomainRegistry.resolve(EncryptionService).verify(plain_password, self.encrypted_password)

    def protect_password(self, plain_password) -> None:
        self.encrypted_password = DomainRegistry.resolve(EncryptionService).encrypt(plain_password)

    def reset_password(self, new_plain_password: str, reset_token: str) -> None:
        assert self.token_with(reset_token), "パスワードのリセットトークンが不正です。"

        self.protect_password(new_plain_password)
        for token in self.tokens_of(Token.Type.PASSWORD_RESET):
            self.tokens.remove(token)

    def token_with(self, value: str) -> Token | None:
        """トークンの値指定で該当トークンを取得できる"""
        for e in self.tokens:
            if e.value == value:
                return e
        return None

    def latest_token_of(self, type: Token.Type) -> Token | None:
        """最新トークンを取得する"""
        latest_token = None
        for e in self.tokens:
            if not e.is_(type):
                continue

            if latest_token is None or latest_token.expires_at < e.expires_at:
                latest_token = e

        return latest_token

    def tokens_of(self, type: Token.Type) -> set[Token]:
        """トークン名指定で全ての該当トークンを取得できる"""
        return {e for e in self.tokens if e.is_(type)}

    def generate(self, type: Token.Type) -> Token:
        """トークンを発行する"""
        token = type.generate()
        self.tokens.add(token)

        if token.is_(Token.Type.VERIFICATION):
            # ドメインイベントを発行する
            DomainEventPublisher\
                .instance()\
                .publish(VerificationTokenGenerated(self.id, self.email_address, token))

        if token.is_(Token.Type.PASSWORD_RESET):
            # ドメインイベントを発行する
            DomainEventPublisher\
                .instance()\
                .publish(PasswordResetTokenGenerated(self.id, self.email_address, token))

        return token

    def verified(self) -> None:
        """ユーザー確認を完了できる"""
        self.enable = True
        self.verified_at = datetime.now()
        for token in self.tokens_of(Token.Type.VERIFICATION):
            self.tokens.remove(token)

    def is_verified(self) -> bool:
        """ユーザー確認が完了されているか判定できる"""
        return self.verified_at is not None

    def is_assigned_to(self, provider: Account.Provider) -> bool:
        """すでに該当プロバイダーと連携済みか"""
        for e in self.accounts:
            if e.provider == provider:
                return True
        return False

    def link(self, account: Account) -> None:
        """アカウント指定でユーザーと連携できる"""
        accounts = set({a for a in self.accounts if a.provider != account.provider})
        accounts.add(account)
        self.accounts = accounts

    def unlink(self, provider: Account.Provider) -> None:
        accounts = set({a for a in self.accounts if a.provider != provider})
        assert len(accounts) > 1 or self.encrypted_password is not None, f"{provider.name} の連携を解除できません。"
        self.accounts = accounts

    def login(self) -> (AccessToken, RefreshToken):
        return AccessToken.generate(self.id)
