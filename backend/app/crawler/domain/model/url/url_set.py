from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

from crawler.domain.model.url import URL


@dataclass(init=False, frozen=True)
class URLSet:
    urls: list[URL]

    def __init__(self, urls: set[URL]):
        for url in urls:
            assert isinstance(url, URL), "URLSet は set[URL] 型を指定してください。"
        super().__setattr__('urls', list(urls))

    def __iter__(self) -> Iterator[URL]:
        for url in self.urls:
            yield url

    def filter_by_regex(self, regex: re.Pattern | str) -> URLSet:
        return URLSet(set(url for url in self.urls if url.match(regex)))
