from typing import override

from crawler.domain.model.interim import Interim
from crawler.port.adapter.service.listing.adapter import ListingAdapter


class ListingAdapterStub(ListingAdapter):
    @override
    def transfer(self, dataset_name: str, interim: Interim) -> None:
        print(dataset_name, interim)
