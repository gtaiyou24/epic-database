from typing import override

from injector import inject

from crawler.domain.model.dataset import DatasetService
from crawler.domain.model.interim import Interim
from crawler.port.adapter.service.dataset.adapter import DatasetAdapter


class DatasetServiceImpl(DatasetService):
    @inject
    def __init__(self, dataset_adapter: DatasetAdapter):
        self.__dataset_adapter = dataset_adapter

    @override
    def transfer(self, dataset_name: str, interim: Interim) -> None:
        self.__dataset_adapter.transfer(dataset_name, interim)
