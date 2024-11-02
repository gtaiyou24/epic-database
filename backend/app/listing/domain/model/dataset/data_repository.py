import abc

from listing.domain.model.dataset import Data, DataId, Dataset


class DataRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, data: Data) -> None:
        pass

    @abc.abstractmethod
    def get(self, dataset_name: Dataset.Name, id: DataId) -> Data | None:
        pass

    @abc.abstractmethod
    def dataset_with(self, dataset_name: Dataset.Name, *args, **kwargs) -> Dataset:
        pass

    @abc.abstractmethod
    def remove(self, data: Data) -> None:
        pass
