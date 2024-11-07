from typing import override

from crawler.domain.model.interim import Interim
from crawler.port.adapter.service.dataset.adapter import DatasetAdapter


class DatasetAdapterStub(DatasetAdapter):
    @override
    def transfer(self, dataset_name: str, interim: Interim) -> None:
        print(dataset_name, interim)
