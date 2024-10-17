from __future__ import annotations

from pydantic import BaseModel, Field

from authority.application.identity.dpo import UserDpo


class UserJson(BaseModel):
    class Account(BaseModel):
        provider: str = Field(title='プロバイダー名')
        provider_account_id: str = Field(title='プロバイダーアカウントID')

        @staticmethod
        def from_(dpo: UserDpo) -> list[UserJson.Account]:
            return [
                UserJson.Account(provider=account.provider.name, provider_account_id=account.provider_account_id)
                for account in dpo.user.accounts
            ]

    id: str = Field(title="id")
    username: str = Field(title="ユーザー名")
    email_address: str = Field(title="メールアドレス")
    accounts: list[Account] = Field(title='連携アカウント一覧', default=[])

    @staticmethod
    def from_(dpo: UserDpo) -> UserJson:
        return UserJson(id=dpo.user.id.value,
                        username=dpo.user.username,
                        email_address=dpo.user.email_address.text,
                        accounts=UserJson.Account.from_(dpo))
