import re

from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class URL:
    value: str

    def __init__(self, value: str):
        assert value, "URLは必須です"
        assert re.match(r"^https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", value) is not None, "http,httpsから始まるURLを指定して下さい"
        super().__setattr__("value", value)

    def __str__(self) -> str:
        return self.value

    def __dir__(self) -> dict:
        return {"url": self.value}
