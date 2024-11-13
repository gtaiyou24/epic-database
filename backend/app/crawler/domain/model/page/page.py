from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup

from crawler.domain.model.page.html import Html
from crawler.domain.model.url import URL, URLSet
from crawler.domain.model.page import HttpStatus


@dataclass(init=False, unsafe_hash=False, frozen=True)
class Page:
    url: URL
    html: Html
    http_status: HttpStatus

    def __init__(self, url: URL, html: Html, http_status: HttpStatus):
        super().__setattr__('url', url)
        super().__setattr__('html', html)
        super().__setattr__('http_status', http_status)

    def __hash__(self):
        return hash(self.url)

    @staticmethod
    def of(url: URL) -> Page:
        return Page(url, Html.empty(), HttpStatus.UNKNOWN)

    def urls(self) -> URLSet:
        return URLSet(self.html.urls(self.url))

    def to_beautiful_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.html.content, features='xml')

    def status_is_200(self) -> bool:
        return self.http_status is HttpStatus.OK
