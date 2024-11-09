from typing import override

from injector import inject

from crawler.domain.model.listing import ListingManagementService
from crawler.domain.model.interim import Interim
from crawler.port.adapter.service.listing.adapter import ListingAdapter


class ListingManagementServiceImpl(ListingManagementService):
    @inject
    def __init__(self, dataset_adapter: ListingAdapter):
        self.__dataset_adapter = dataset_adapter

    @override
    def transfer(self, dataset_name: str, interim: Interim) -> None:
        self.__dataset_adapter.transfer(dataset_name, interim)
