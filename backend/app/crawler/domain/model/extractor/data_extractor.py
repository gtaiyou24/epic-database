import abc

from crawler.domain.model.interim import Interim
from crawler.domain.model.data import Data
from crawler.domain.model.page import Page


class DataExtractor(abc.ABC):
    """抽出器の抽象クラス"""

    @abc.abstractmethod
    def extract(self, data_object: Interim, page: Page) -> Data | None:
        pass
