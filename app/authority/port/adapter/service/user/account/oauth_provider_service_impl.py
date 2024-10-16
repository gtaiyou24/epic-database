from typing import override, Literal

from authority.domain.model.user.account import OAuthProviderService, Account, Profile
from authority.port.adapter.service.user.account.adapter import OAuthProviderAdapter


class OAuthProviderServiceImpl(OAuthProviderService):
    @override
    def authenticate(self,
                     provider: Literal['GOOGLE'],
                     code: str,
                     redirect_uri: str,
                     code_verifier: str | None,
                     grant_type: str) -> (Profile, Account):
        return OAuthProviderAdapter.Provider[provider].authenticate(code, redirect_uri, code_verifier, grant_type)
