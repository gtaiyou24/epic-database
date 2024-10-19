from injector import inject

from common.application import transactional
from listing.application.company.command import SaveCompanyCommand
from listing.domain.model.company import CompanyRepository, Company, CompanyId
from listing.domain.model.url import URL


class CompanyApplicationService:
    @inject
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    @transactional
    def save(self, command: SaveCompanyCommand) -> None:
        company_id = None
        for id in command.company_ids:
            id = CompanyId.Type[id.type].make(id.value)

            if company_id is None:
                company_id = id
            else:
                company_id.set_other_id(id)

        company = Company(
            company_id,
            command.name,
            command.description,
            command.founded_at,
            URL(command.homepage),
            list([URL(url) for url in command.same_as])
        )
        self.company_repository.add(company)
