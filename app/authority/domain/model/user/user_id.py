import re
from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class UserId:
    value: str

    def __init__(self, value: str):
        assert value, "ユーザーIDは必須です。"
        assert re.match(r"([0-9a-f]{8})-([0-9a-f]{4})-(4[0-9a-f]{3})-([0-9a-f]{4})-([0-9a-f]{12})", value), \
            "ユーザーIDには UUID を指定してください。"
        super().__setattr__("value", value)
