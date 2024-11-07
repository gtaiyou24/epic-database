from typing import override

from crawler.domain.model.interim import InterimRepository, Interim, InterimId


class InMemInterimRepository(InterimRepository):
    interims: set[Interim] = set()

    @override
    def save(self, interim: Interim) -> None:
        self.interims.add(interim)

    @override
    def get(self, id: InterimId) -> Interim | None:
        for interim in self.interims:
            if interim.id == id:
                return interim
        return None

    @override
    def interims_with_source(self, source: Interim.Source) -> set[Interim]:
        return {interim for interim in self.interims if interim.source == source}

    @override
    def remove(self, interim: Interim) -> None:
        self.interims.remove(interim)
