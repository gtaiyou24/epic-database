from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from authority.domain.model.user.account import ProviderTokens


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Account:
    """アカウント

    ユーザーは複数のアカウントを持つことができる。アカウントは、ユーザーが初めてサインインするプロバイダーの種類ごとに作成される。
    たとえば、あるユーザーがGoogleでサインインし、次にFacebookでサインインした場合、プロバイダごとに2つのアカウントを持つことになります。
    ユーザーが最初にサインインしたプロバイダーが、ユーザー・オブジェクトの作成にも使われます。
    """
    class Provider(Enum):
        FACEBOOK = 'facebook'
        GOOGLE = 'google'
        LINE = 'line'
        X = 'x'

        def make(self,
                 provider_account_id: str,
                 tokens: ProviderTokens,
                 scope: str,
                 id_token: str) -> Account:
            return Account(self, provider_account_id, tokens, scope, id_token)

    provider: Provider
    provider_account_id: str
    tokens: ProviderTokens
    scope: str
    id_token: str
