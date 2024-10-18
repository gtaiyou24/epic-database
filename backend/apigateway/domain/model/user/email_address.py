import re
from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, eq=True, frozen=True)
class EmailAddress:
    text: str

    def __init__(self, text: str):
        assert text, "メールアドレスは必須です。"
        assert 0 < len(text) <= 100, "メールアドレスは100文字以下である必要があります。"
        assert re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", text), "メールアドレスが不正です。"
        super().__setattr__("text", text)

    def __str__(self):
        return self.text

    @property
    def domain(self) -> str:
        return self.text.split("@")[1]
