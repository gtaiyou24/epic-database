from __future__ import annotations

import json
from datetime import date, datetime

from sqlalchemy import UniqueConstraint, Index, VARCHAR, Integer, TEXT, DATE, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.port.adapter.persistence.repository.mysql import DataBase
from dataset.domain.model.company import Company, CompanyId, Summary, Address, ContactPoint
from dataset.domain.model.company.address import Prefecture
from dataset.domain.model.url import URL


class CompanyRelatedPagesTableRow(DataBase):
    __tablename__ = 'company_related_pages'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'company_id')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="ID")
    company_id: Mapped[str] = mapped_column(
        ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    url: Mapped[str] = mapped_column(TEXT, nullable=False, comment="関連ページのURL")

    company: Mapped[CompaniesTableRow] = relationship("CompaniesTableRow", back_populates="related_pages")

    @staticmethod
    def create(company: Company) -> list[CompanyRelatedPagesTableRow]:
        return [
            CompanyRelatedPagesTableRow(
                company_id=company.id.type_of(CompanyId.Type.UUID).value,
                url=url.address
            ) for url in company.same_as
        ]

    def to_value(self) -> URL:
        return URL(self.url)


class CompanySummariesTableRow(DataBase):
    __tablename__ = 'company_summaries'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'company_id')),
        (UniqueConstraint("company_id", name=f"uix_{__tablename__}_1")),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="ID")
    company_id: Mapped[str] = mapped_column(
        ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    payload: Mapped[str] = mapped_column(JSONB, nullable=False)

    company: Mapped[CompaniesTableRow] = relationship("CompaniesTableRow", back_populates="summaries")

    @staticmethod
    def create(company: Company) -> CompanySummariesTableRow:
        return CompanySummariesTableRow(
            company_id=company.id.type_of(CompanyId.Type.UUID).value,
            payload=json.dumps({summary.name.name: summary.value for summary in company.summaries})
        )

    def to_value(self) -> set[Summary]:
        return {Summary(Summary.Name[name], value) for name, value in json.loads(self.payload).items()}


class CompanyOfficesTableRow(DataBase):
    __tablename__ = 'company_offices'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'company_id')),
        (UniqueConstraint("company_id", "country", "prefecture", "city", "street", name=f"uix_{__tablename__}_1")),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="ID")
    company_id: Mapped[str] = mapped_column(
        ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    country: Mapped[str] = mapped_column(VARCHAR(10), nullable=False, comment='国')
    postal_code: Mapped[str | None] = mapped_column(VARCHAR(7), nullable=True, comment='郵便番号')
    prefecture: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="都道府県")
    city: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="市町村")
    street: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="番地/建物")

    company: Mapped[CompaniesTableRow] = relationship("CompaniesTableRow", back_populates="offices")

    @staticmethod
    def create(company: Company) -> list[CompanyOfficesTableRow]:
        return [CompanyOfficesTableRow(
            company_id=company.id.type_of(CompanyId.Type.UUID).value,
            country=office.country,
            postal_code=office.postal_code,
            prefecture=office.prefecture.name,
            city=office.city,
            street=office.street
        ) for office in company.offices]

    def to_value(self) -> Address:
        return Address(self.country, self.postal_code, Prefecture[self.prefecture], self.city, self.street)


class CompanyContactPointsTableRow(DataBase):
    __tablename__ = 'company_contact_points'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'company_id')),
        (UniqueConstraint('company_id', 'type', 'value', name=f'uix_{__tablename__}_1')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="ID")
    company_id: Mapped[str] = mapped_column(
        ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    type: Mapped[str] = mapped_column(VARCHAR(10), nullable=False, comment='お問い合わせタイプ')
    value: Mapped[str] = mapped_column(TEXT, nullable=False, comment='お問い合わせ先')

    company: Mapped[CompaniesTableRow] = relationship("CompaniesTableRow", back_populates="contact_points")

    @staticmethod
    def create(company: Company) -> list[CompanyContactPointsTableRow]:
        return [CompanyContactPointsTableRow(
            company_id=company.id.type_of(CompanyId.Type.UUID).value,
            type=contact_point.type.name,
            value=contact_point.value
        ) for contact_point in company.contact_points]

    def to_value(self) -> ContactPoint:
        return ContactPoint.Type[self.type].make(self.value)


class CompaniesTableRow(DataBase):
    __tablename__ = 'companies'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'corporate_number')),
        (UniqueConstraint("corporate_number", name=f"uix_{__tablename__}_1")),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, nullable=False, comment="UUID")
    corporate_number: Mapped[str] = mapped_column(VARCHAR(13), nullable=False, comment="法人番号")
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="企業名")
    description: Mapped[str] = mapped_column(TEXT, nullable=True, comment="企業の概略")
    founded_at: Mapped[date] = mapped_column(DATE, nullable=True, comment="創業日")
    homepage: Mapped[str | None] = mapped_column(TEXT, nullable=True, comment="ホームページURL")

    related_pages: Mapped[list[CompanyRelatedPagesTableRow]] = relationship(back_populates="company", lazy='joined')
    summaries: Mapped[CompanySummariesTableRow] = relationship(back_populates="company", lazy='joined', uselist=False)
    contact_points: Mapped[list[CompanyContactPointsTableRow]] = relationship(back_populates="company", lazy='joined')
    offices: Mapped[list[CompanyOfficesTableRow]] = relationship(back_populates="company", lazy='joined')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now())

    @staticmethod
    def create(company: Company) -> CompaniesTableRow:
        return CompaniesTableRow(
            id=company.id.type_of(CompanyId.Type.UUID).value,
            corporate_number=company.id.type_of(CompanyId.Type.JCN).value,
            name=company.name,
            description=company.description,
            founded_at=company.founded_at,
            homepage=company.homepage.address if company.homepage else None,
            related_pages=CompanyRelatedPagesTableRow.create(company),
            summaries=CompanySummariesTableRow.create(company),
            contact_points=CompanyContactPointsTableRow.create(company),
            offices=CompanyOfficesTableRow.create(company),
        )

    def update(self, company: Company) -> None:
        self.name = company.name
        self.description = company.description

    def to_entity(self) -> Company:
        return Company(
            id=CompanyId.of(self.id).set_other_id(CompanyId.of(self.corporate_number)),
            name=self.name,
            description=self.description,
            founded_at=self.founded_at,
            homepage=URL(self.homepage) if self.homepage else None,
            same_as=[tr.to_value() for tr in self.related_pages],
            summaries=self.summaries.to_value(),
            contact_points={tr.to_value() for tr in self.contact_points},
            offices={tr.to_value() for tr in self.offices}
        )
