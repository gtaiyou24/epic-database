from dataclasses import dataclass

from dataset.domain.model.company import CompanyId
from dataset.domain.model.person import PersonId


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Employee:
    company_id: CompanyId
    role: str
    person_id: PersonId
