from multiprocessing import Pool

from crawler.domain.model.interim import Interim
from crawler.domain.model.data import Data
from crawler.domain.model.extractor import DataExtractor
from crawler.domain.model.page import Page


class AsyncExtractor:
    def __init__(self, data_object: Interim, page: Page):
        self.data_object = data_object
        self.page = page

    def extract(self, data_extractor: DataExtractor) -> Data | None:
        return data_extractor.extract(self.data_object, self.page)


class DataExtractors:
    def __init__(self, extractors: list[DataExtractor]):
        self.extractors = extractors

    def extract(self, data_object: Interim, page: Page) -> set[Data]:
        # 並列で抽出
        async_extractor = AsyncExtractor(data_object, page)
        pool = Pool(10)

        # 実行
        data_set = pool.map(async_extractor.extract, self.extractors)

        return {data for data in data_set if data is not None}
