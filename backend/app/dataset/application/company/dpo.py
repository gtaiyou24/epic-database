from dataclasses import dataclass

from dataset.domain.model.company import Company


@dataclass(init=True, unsafe_hash=True, frozen=True)
class CompanyDpo:
    company: Company
