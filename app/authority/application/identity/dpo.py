from dataclasses import dataclass

from authority.domain.model.user import User


@dataclass(init=True, unsafe_hash=True, frozen=True)
class UserDpo:
    user: User
