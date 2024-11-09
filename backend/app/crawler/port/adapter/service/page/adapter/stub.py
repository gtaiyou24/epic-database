from typing import override

from crawler.domain.model.page import Page
from crawler.domain.model.url import URL
from crawler.port.adapter.service.page.adapter import SearchEngineAdapter


class SearchEngineAdapterStub(SearchEngineAdapter):
    @override
    def search(self, keyword: str) -> Page:
        return Page.of(URL(f'https://google.com/search?q={keyword}'))

    @override
    def fetch(self, url: URL) -> Page:
        return Page.of(url)
