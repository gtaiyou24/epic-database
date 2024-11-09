import abc

from crawler.domain.model.interim import Interim


class ListingManagementService(abc.ABC):
    @abc.abstractmethod
    def transfer(self, dataset_name: str, interim: Interim) -> None:
        pass
