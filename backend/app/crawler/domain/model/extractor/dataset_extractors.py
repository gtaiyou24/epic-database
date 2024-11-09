from multiprocessing import Pool

from crawler.domain.model.interim import Interim
from crawler.domain.model.data import Data, DataSet
from crawler.domain.model.extractor import DataExtractor
from crawler.domain.model.page import Page


class AsyncExtractor:
    def __init__(self, data_object: Interim, page: Page):
        self.data_object = data_object
        self.page = page

    def extract(self, data_extractor: DataExtractor) -> Data | None:
        return data_extractor.extract(self.data_object, self.page)


class DataSetExtractors:
    def __init__(self, extractors: list[DataExtractor]):
        self.__extractors = extractors

    def extract(self, data_object: Interim, page: Page) -> DataSet:
        # 並列で抽出
        async_extractor = AsyncExtractor(data_object, page)
        pool = Pool(10)

        # 実行
        data_set = pool.map(async_extractor.extract, self.__extractors)

        return DataSet({data for data in data_set if data is not None})
