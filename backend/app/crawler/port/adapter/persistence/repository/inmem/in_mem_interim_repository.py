from typing import override

from crawler.domain.model.interim import InterimRepository, Interim, InterimId


class InMemInterimRepository(InterimRepository):
    interim_payloads: set[Interim] = set()

    @override
    def save(self, interim: Interim) -> None:
        self.interim_payloads.add(interim)

    @override
    def get(self, id: InterimId) -> Interim | None:
        for interim_payload in self.interim_payloads:
            if interim_payload.id == id:
                return interim_payload
        return None

    @override
    def remove(self, interim: Interim) -> None:
        self.interim_payloads.remove(interim)
