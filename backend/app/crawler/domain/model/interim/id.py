from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Id:
    value: str

    def __init__(self, value: str):
        assert value, "IDは必須です。"
        super().__setattr__("value", value)
