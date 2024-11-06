from typing import override

from injector import inject

from crawler.domain.model.interim import InterimRepository, Interim, InterimId
from crawler.port.adapter.persistence.repository.mysql.interim import CacheLayerInterim


class MySQLInterimRepository(InterimRepository):
    @inject
    def __init__(self, cache_layer_interim: CacheLayerInterim):
        self.__cache_layer_interim = cache_layer_interim

    @override
    def save(self, interim: Interim) -> None:
        self.__cache_layer_interim.set(interim)

    @override
    def get(self, id: InterimId) -> Interim | None:
        return self.__cache_layer_interim.cache_or_origin(id)

    @override
    def remove(self, interim: Interim) -> None:
        self.__cache_layer_interim.delete(interim)
