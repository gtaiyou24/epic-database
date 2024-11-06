import abc
import uuid

from crawler.domain.model.interim import Interim, InterimId


class InterimRepository(abc.ABC):
    def next_identity(self) -> InterimId:
        return InterimId.Type.UUID.make(str(uuid.uuid4()))

    @abc.abstractmethod
    def save(self, interim: Interim) -> None:
        pass

    @abc.abstractmethod
    def get(self, id: InterimId) -> Interim | None:
        pass

    @abc.abstractmethod
    def remove(self, interim: Interim) -> None:
        pass
