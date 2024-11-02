from __future__ import annotations

import abc
from dataclasses import dataclass
from enum import Enum


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateCommand(abc.ABC):
    class OAuthType(Enum):
        CREDENTIAL = 'email_password'
        GOOGLE = 'google'
        GITHUB = 'github'

    oauth_type: OAuthType
