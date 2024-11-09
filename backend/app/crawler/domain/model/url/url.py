from __future__ import annotations

import re
from dataclasses import dataclass

from urllib.parse import urljoin


@dataclass(init=False, unsafe_hash=False, frozen=True)
class URL:
    JAVASCRIPT_VOID_REGEX = re.compile(r"^javascript:void\([0-9]+\);$")
    ABSOLUTE_URL_REGEX = re.compile(r"^(https|http)?://[\w/:%#\$&\?\(\)~\.=\+\-]+")

    absolute: str

    def __init__(self, absolute_url: str):
        assert absolute_url is not None, "Noneが指定されています。絶対パスを指定してください。"
        assert self.JAVASCRIPT_VOID_REGEX.match(absolute_url) is None, "javascript.voidが指定されています。"
        assert self.ABSOLUTE_URL_REGEX.match(absolute_url), f"{absolute_url}は絶対パスではありません。絶対パスを指定してください。"

        super().__setattr__("absolute", re.sub(r"#.*$", "", absolute_url))

    @staticmethod
    def of(path: str, url: URL) -> URL:
        assert path is not None, "Noneが指定されています。絶対パスを指定してください。"

        if URL.ABSOLUTE_URL_REGEX.match(path):
            return URL(path)
        return URL(urljoin(url.absolute, path))

    def match(self, regex: re.Pattern | str) -> bool:
        if isinstance(regex, str):
            regex = re.compile(regex)
        return regex.match(self.absolute) is not None

    def __hash__(self):
        return hash(self.absolute)

    def __eq__(self, other):
        if (other is None) or (not isinstance(other, URL)):
            return False
        return self.absolute == other.absolute

    def __str__(self):
        return self.absolute
