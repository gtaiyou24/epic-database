from dataclasses import dataclass

from listing.domain.model.company import CompanyId
from listing.domain.model.person import PersonId


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Employee:
    company_id: CompanyId
    role: str
    person_id: PersonId
