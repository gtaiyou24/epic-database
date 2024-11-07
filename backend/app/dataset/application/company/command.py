from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(init=True, unsafe_hash=True, frozen=True)
class SaveCompanyCommand:
    @dataclass(init=True, unsafe_hash=True, frozen=True)
    class Address:
        country: str
        postal_code: str
        prefecture: str
        city: str
        street: str

    uuid: str | None
    corporate_number: str
    name: str
    description: str
    founded_at: datetime
    homepage: str | None
    same_as: list[str]
    summaries: dict[str, Any]
    contact_points: list[dict[str, Any]]
    offices: list[Address]

    def contact_point_items(self):
        for contact_point in self.contact_points:
            for type, value in contact_point.items():
                yield type, value
