import re

from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class URL:
    address: str

    def __init__(self, address: str):
        assert address, "URLは必須です"
        assert re.match(r"^https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", address) is not None, "http,httpsから始まるURLを指定して下さい"
        super().__setattr__("address", address)

    def __str__(self) -> str:
        return self.address

    def __dir__(self) -> dict:
        return {"url": self.address}
