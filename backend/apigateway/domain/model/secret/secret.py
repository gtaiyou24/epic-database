from dataclasses import dataclass
from enum import Enum


class Key(Enum):
    JWT_PRIVATE = 'jwt_private_key'
    JWT_PUBLIC = 'jwt_public_key'


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Secret:
    key: Key
    version: float
    value: str
