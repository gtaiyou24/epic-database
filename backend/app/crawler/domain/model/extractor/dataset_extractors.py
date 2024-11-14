import asyncio
from typing import List
from crawler.domain.model.interim import Interim
from crawler.domain.model.data import Data, DataSet
from crawler.domain.model.extractor import DataExtractor
from crawler.domain.model.page import Page


class AsyncExtractor:
    def __init__(self, data_object: Interim, page: Page):
        assert isinstance(data_object, Interim), f"data_object {data_object} must be an Interim object"
        assert isinstance(page, Page), f"page {page} must be an Page object"
        self.data_object = data_object
        self.page = page

    async def extract(self, data_extractor: DataExtractor) -> Data | None:
        # 各データ抽出器の `extract` メソッドを非同期に呼び出し
        return await asyncio.to_thread(data_extractor.extract, self.data_object, self.page)


class DataSetExtractors:
    def __init__(self, extractors: List[DataExtractor]):
        self.__extractors = extractors

    async def extract(self, data_object: Interim, page: Page) -> DataSet:
        async_extractor = AsyncExtractor(data_object, page)

        # asyncio.gatherを使用して並列実行
        tasks = [async_extractor.extract(extractor) for extractor in self.__extractors]
        data_set = await asyncio.gather(*tasks)

        # Noneでない結果のみを DataSet に追加
        return DataSet({data for data in data_set if data is not None})
