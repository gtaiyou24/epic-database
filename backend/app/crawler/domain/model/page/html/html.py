from __future__ import annotations

from dataclasses import dataclass
from typing import Set

from bs4 import BeautifulSoup
from crawler.domain.model.page.html import CharacterCode
from crawler.domain.model.url import URL


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Html:
    content: str | None
    character_code: CharacterCode | None

    def __init__(self, text: str | None, character_code: CharacterCode | None):
        super().__setattr__("text", text)
        super().__setattr__("character_code", character_code)

    @staticmethod
    def empty() -> Html:
        return Html(None, None)

    def is_empty(self) -> bool:
        return (self.content is None) or (self.content == "")

    def urls(self, base_url: URL) -> Set[URL]:
        url_set = set()
        if self.content is None:
            return url_set

        for link in BeautifulSoup(self.content, "lxml").find_all("a"):
            try:
                url = URL.of(link.get("href"), base_url)
                url_set.add(url)
            except AssertionError:
                continue

        return url_set
