import uuid
from typing import override

from injector import inject

from listing.domain.model.company import CompanyRepository, Company, CompanyId
from listing.port.adapter.persistence.repository.mysql.company import CacheLayerCompany


class MySQLCompanyRepository(CompanyRepository):
    @inject
    def __init__(self, cache_layer_company: CacheLayerCompany):
        self.__cache_layer_company = cache_layer_company

    @override
    def next_identity(self) -> CompanyId:
        return CompanyId.Type.UUID.make(str(uuid.uuid4()))

    @override
    def add(self, company: Company) -> None:
        self.__cache_layer_company.set(company)

    @override
    def get(self, company_id: CompanyId) -> Company | None:
        return self.__cache_layer_company.cache_or_origin(company_id)

    @override
    def companies_with_ids(self, *company_id: tuple[CompanyId]) -> list[Company]:
        pass

    @override
    def remove(self, company: Company) -> None:
        pass
