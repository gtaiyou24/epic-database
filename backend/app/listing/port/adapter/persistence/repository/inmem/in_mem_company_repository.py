import uuid
from typing import override

from listing.domain.model.company import CompanyRepository, Company, CompanyId


class InMemCompanyRepository(CompanyRepository):
    @override
    def next_identity(self) -> CompanyId:
        return CompanyId.Type.UUID.make(str(uuid.uuid4()))

    @override
    def add(self, company: Company) -> None:
        pass

    @override
    def get(self, company_id: CompanyId) -> Company | None:
        pass

    @override
    def companies_with_ids(self, *company_id: tuple[CompanyId]) -> list[Company]:
        pass

    @override
    def remove(self, company: Company) -> None:
        pass
