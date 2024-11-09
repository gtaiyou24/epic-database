import abc

from listing.domain.model.company import Company, CompanyId


class CompanyRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> CompanyId:
        pass

    @abc.abstractmethod
    def add(self, company: Company) -> None:
        pass

    @abc.abstractmethod
    def get(self, company_id: CompanyId) -> Company | None:
        pass

    @abc.abstractmethod
    def companies_with_ids(self, *company_id: tuple[CompanyId]) -> list[Company]:
        pass

    @abc.abstractmethod
    def remove(self, company: Company) -> None:
        pass
