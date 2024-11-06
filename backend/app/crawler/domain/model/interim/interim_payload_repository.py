import abc

from crawler.domain.model.interim import InterimPayload, Id


class InterimPayloadRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, interim_payload: InterimPayload) -> None:
        pass

    @abc.abstractmethod
    def get(self, id: Id) -> InterimPayload | None:
        pass

    @abc.abstractmethod
    def remove(self, interim_payload: InterimPayload) -> None:
        pass
