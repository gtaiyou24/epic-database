import abc
from typing import override

from lxml import html

from crawler.domain.model.interim import Interim
from crawler.domain.model.data import Data
from crawler.domain.model.page import Page


class DataExtractor(abc.ABC):
    """抽出器の抽象クラス"""

    @abc.abstractmethod
    def extract(self, data_object: Interim, page: Page) -> Data | None:
        pass


class CssSelector(DataExtractor):
    def __init__(self,
                 name: str, css_selector: str,
                 attribute: str | None = None):
        self.__name = name
        self.__css_selector = css_selector
        self.__attribute = attribute

    @override
    def extract(self, data_object: Interim, page: Page) -> Data | None:
        tag = page.to_beautiful_soup().select_one(self.__css_selector)
        if tag is None:
            return None
        return Data(self.__name, tag.get(self.__attribute) if self.__attribute else tag.text)


class XPathSelector(DataExtractor):
    def __init__(self, name: str, xpath: str):
        self.__name = name
        self.__xpath = xpath

    @override
    def extract(self, data_object: Interim, page: Page) -> Data | None:
        lxml = html.fromstring(str(page.to_beautiful_soup()))
        r = lxml.xpath(self.__xpath)
        if not len(r):
            return None
        return Data(self.__name, r[0] if isinstance(r[0], str) else r[0].text)


class TableRowExtractor(DataExtractor):
    def __init__(self,
                 name: str,
                 th: str):
        self.__name = name
        self.__th_text = th

    @override
    def extract(self, data_object: Interim, page: Page) -> Data | None:
        th = page.to_beautiful_soup().select_one(f'th:-soup-contains("{self.__th_text}")')
        if not th:
            return None
        # 同じ行 (tr タグ) 内の td タグを取得
        td = th.find_next_sibling("td")
        if not td:
            return None
        return Data(self.__name, td.text)
