from __future__ import annotations

import re
from dataclasses import dataclass

from crawler.domain.model.url import URL


@dataclass(init=False, frozen=True)
class URLSet:
    urls: set[URL]

    def __init__(self, urls: set[URL]):
        super().__setattr__('urls', urls)

    def filter_by_regex(self, regex: re.Pattern) -> URLSet:
        return URLSet(set(url for url in self.urls if url.match(regex)))
