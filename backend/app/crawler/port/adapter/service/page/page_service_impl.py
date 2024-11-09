from typing import override

from injector import inject

from crawler.domain.model.page import Page, PageService
from crawler.domain.model.url import URL
from crawler.port.adapter.service.page.adapter import SearchEngineAdapter


class PageServiceImpl(PageService):
    @inject
    def __init__(self, search_engine_adapter: SearchEngineAdapter):
        self.__search_engine_adapter = search_engine_adapter

    @override
    def search(self, keyword: str) -> Page:
        return self.__search_engine_adapter.search(keyword)

    @override
    def fetch(self, url: URL) -> Page:
        return self.__search_engine_adapter.fetch(url)
