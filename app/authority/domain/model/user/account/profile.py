from dataclasses import dataclass

from authority.domain.model.mail import EmailAddress


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Profile:
    username: str
    email_address: EmailAddress
    image_url: str
