from dataclasses import dataclass

from authority.domain.model.token import AccessToken, RefreshToken


@dataclass(init=True, unsafe_hash=True, frozen=True)
class TokenDpo:
    access_token: AccessToken
    refresh_token: RefreshToken
