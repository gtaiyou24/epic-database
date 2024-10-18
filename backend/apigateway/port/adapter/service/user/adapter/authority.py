from typing import override

from apigateway.domain.model.user import Account, Tokens, User, UserId, EmailAddress
from apigateway.port.adapter.service.user.adapter import IdentityAccessAdapter
from authority.port.adapter.resource.auth import AuthResource


class AuthorityAdapter(IdentityAccessAdapter):
    def __init__(self):
        self.__auth_resource = AuthResource()

    @override
    def authenticate(self, access_token: str) -> User:
        dpo = self.__auth_resource.authorization_application_service.identify(access_token)
        return User(
            id=UserId(dpo.user.id.value),
            username=dpo.user.username,
            email_address=EmailAddress(dpo.user.email_address.text),
            enable=dpo.user.enable,
            accounts={
                Account(
                    provider=account.provider.name,
                    provider_account_id=account.provider_account_id,
                    tokens=Tokens(
                        access_token=account.tokens.access_token,
                        refresh_token=account.tokens.refresh_token,
                        expires_at=account.tokens.expires_at,
                        token_type=account.tokens.token_type.name,
                    ),
                    scope=account.scope,
                    id_token=account.id_token
                ) for account in dpo.user.accounts
            },
            verified_at=dpo.user.verified_at,
        )
