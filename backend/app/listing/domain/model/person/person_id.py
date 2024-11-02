import re
from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class PersonId:
    value: str

    def __init__(self, value: str):
        assert value, "人物IDは必須です。"
        assert re.match(r"([0-9a-f]{8})-([0-9a-f]{4})-(4[0-9a-f]{3})-([0-9a-f]{4})-([0-9a-f]{12})", value), \
            "人物IDには UUID を指定してください。"
        super().__setattr__("value", value)
