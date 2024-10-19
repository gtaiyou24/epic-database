from datetime import datetime


class SaveCompanyCommand:
    class CompanyId:
        type: str
        value: str

    company_ids: set[CompanyId]
    name: str
    description: str
    founded_at: datetime
    homepage: str
    same_as: list[str]
