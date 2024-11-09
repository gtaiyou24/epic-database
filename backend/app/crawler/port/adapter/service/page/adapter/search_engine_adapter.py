import abc

from crawler.domain.model.page import Page
from crawler.domain.model.url import URL


class SearchEngineAdapter(abc.ABC):
    @abc.abstractmethod
    def search(self, keyword: str) -> Page:
        pass

    @abc.abstractmethod
    def fetch(self, url: URL) -> Page:
        pass
