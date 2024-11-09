from injector import inject

from common.application import transactional
from common.exception import SystemException, ErrorCode
from listing.application.company.command import SaveCompanyCommand
from listing.application.company.dpo import CompanyDpo
from listing.domain.model.company import CompanyRepository, Company, CompanyId, Summary, ContactPoint, Address
from listing.domain.model.company.address import Prefecture
from listing.domain.model.url import URL


class CompanyApplicationService:
    @inject
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    @transactional(is_listening=True)
    def save(self, command: SaveCompanyCommand) -> CompanyDpo:
        company = self.company_repository.get(CompanyId.of(command.corporate_number))

        company_id = CompanyId.of(command.corporate_number)
        if company is None:
            company_id = company_id.set_other_id(self.company_repository.next_identity())
        else:
            company_id = company_id.set_other_id(company.id.type_of(CompanyId.Type.UUID))

        company = Company(
            company_id,
            command.name,
            command.description,
            command.founded_at,
            URL(command.homepage) if command.homepage else None,
            list([URL(url) for url in command.same_as]),
            {Summary.Name.value_of(name).make(value) for name, value in command.summaries.items()},
            {ContactPoint.Type.value_of(type).make(value) for type, value in command.contact_point_items()},
            {Address(
                office.country,
                office.postal_code,
                Prefecture.value_of(office.prefecture),
                office.city,
                office.street
            ) for office in command.offices},
        )
        self.company_repository.add(company)
        return CompanyDpo(company=company)

    def company_with_id(self, id: str) -> CompanyDpo:
        company_id = CompanyId.of(id)
        company = self.company_repository.get(company_id)
        if company is None:
            raise SystemException(ErrorCode.COMPANY_NOT_FOUND, f"企業 {id} が見つかりませんでした")
        return CompanyDpo(company=company)
