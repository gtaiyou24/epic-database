from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateEmailPasswordCommand:
    email_address: str
    plain_password: str

    def __str__(self):
        return f"{'email_address': {self.email_address}, 'plain_password': {self.plain_password[0:1]}...}"


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateAccountCommand:
    provider: Literal['GOOGLE']
    code: str
    redirect_uri: str
    code_verifier: str
    grant_type: str

    def __str__(self):
        return f"""{
    'provider': {self.provider},
    'code': {self.code}, 
    'redirect_uri': {self.redirect_uri}, 
    'code_verifier': {self.code_verifier}, 
    'grant_type': {self.grant_type}
}"""


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RefreshCommand:
    refresh_token: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RevokeCommand:
    token: str
