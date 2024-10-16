from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RegisterUserCommand:
    @dataclass(init=True, unsafe_hash=True, frozen=True)
    class Tenant:
        name: str

    @dataclass(init=True, unsafe_hash=True, frozen=True)
    class User:
        username: str
        email_address: str
        plain_password: str

    tenant: Tenant
    user: User


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ForgotPasswordCommand:
    email_address: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ResetPasswordCommand:
    reset_token: str
    password: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ChangePasswordCommand:
    user_id: str
    new_password: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class SaveUserCommand:
    user_id: str
    username: str
    email_address: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class DeleteUserCommand:
    user_id: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class LinkAccountCommand:
    user_id: str
    provider: Literal["GOOGLE"]
    code: str
    redirect_uri: str
    code_verifier: str
    grant_type: str

    def __str__(self):
        return f"""{
'user_id': {self.user_id},
'provider': {self.provider},
'code': {self.code}, 
'redirect_uri': {self.redirect_uri}, 
'code_verifier': {self.code_verifier}, 
'grant_type': {self.grant_type}
}"""


@dataclass(init=True, unsafe_hash=True, frozen=True)
class UnlinkAccountCommand:
    user_id: str
    provider: Literal["GOOGLE"]