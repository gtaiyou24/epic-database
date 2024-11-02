import abc
from typing import Literal

from authority.domain.model.user.account import Account, Profile


class OAuthProviderService(abc.ABC):
    """認証プロバイダー

    Google や Facebook, X, Instagram, GitHub などの認証プロバイダーに対して認証を行い、アカウント情報を取得するドメインサービス
    """
    @abc.abstractmethod
    def authenticate(self,
                     provider: Literal['GOOGLE'],
                     code: str,
                     redirect_uri: str,
                     code_verifier: str | None,
                     grant_type: str) -> (Profile, Account):
        pass
