from __future__ import annotations

from sqlalchemy import UniqueConstraint, Index, VARCHAR, Integer, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from common.port.adapter.persistence.repository.mysql import DataBase
from listing.domain.model.company import Company, CompanyId


class CompanyIdMappingsTableRow(DataBase):
    __tablename__ = 'company_id_mappings'
    __table_args__ = (
        (UniqueConstraint("company_id", "type", name=f"uix_{__tablename__}_1")),
        (UniqueConstraint("other_id", name=f"uix_{__tablename__}_2")),
        (Index(f'idx_{__tablename__}_1', 'other_id', 'type')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    uuid: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, nullable=False, comment="UUID")
    other_id: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="UUID以外の企業ID")
    type: Mapped[int] = mapped_column(Integer, nullable=False, comment="IDタイプ")


class CompaniesTableRow(DataBase):
    __tablename__ = 'companies'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'product_id', 'type')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, nullable=False, comment="UUID")
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="企業名")
    description: Mapped[str] = mapped_column(TEXT, nullable=True, comment="企業の概略")

    @staticmethod
    def create(company: Company) -> CompaniesTableRow:
        return CompaniesTableRow(
            id=company.id.type_of(CompanyId.Type.UUID).value,
            name=company.name,
            description=company.description,
        )

    def update(self, company: Company) -> None:
        self.name = company.name
        self.description = company.description

    def to_entity(self) -> Company:
        return Company(
            id=CompanyId.of(self.id) \
                .set_other_id(CompanyId.of(self.isin_code)) \
                .set_other_id(CompanyId.of(self.ita_code)),
            name=self.name,
            description=self.description,
        )
