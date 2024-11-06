import abc

from crawler.domain.model.interim import Interim, InterimId


class InterimRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, interim: Interim) -> None:
        pass

    @abc.abstractmethod
    def get(self, id: InterimId) -> Interim | None:
        pass

    @abc.abstractmethod
    def remove(self, interim: Interim) -> None:
        pass
