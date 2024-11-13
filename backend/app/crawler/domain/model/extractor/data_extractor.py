from __future__ import annotations

from typing import override, Callable

from lxml import html

from crawler.domain.model.interim import Interim
from crawler.domain.model.data import Data
from crawler.domain.model.page import Page


class DataExtractor:
    """抽出器の抽象クラス"""
    def __init__(self,
                 extractor: DataExtractor,
                 processor_pipeline: list[Callable[[str], str]] = []):
        self.__extractor = extractor
        self.__processor_pipeline = processor_pipeline

    def extract(self, data_object: Interim, page: Page) -> Data | None:
        data = self.__extractor.extract(data_object, page)

        if data is None:
            return None

        value = str(data.value())
        for processor in self.__processor_pipeline:
            value = processor(value)
            if value is None:
                return None

        return Data(data.name(), value)


class CssSelector(DataExtractor):
    def __init__(self,
                 name: str,
                 css_selector: str,
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
    def __init__(self, name: str, th: str):
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
