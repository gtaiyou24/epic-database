from injector import inject
from sqlalchemy import or_
from sqlalchemy.orm import Query

from common.application import UnitOfWork
from common.port.adapter.persistence.repository.mysql import MySQLUnitOfWork
from dataset.domain.model.company import Company, CompanyId
from dataset.port.adapter.persistence.repository.mysql.company.table import CompaniesTableRow


class DriverManagerCompany:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_by_id(self, company_id: CompanyId) -> Company | None:
        with self.__unit_of_work.query() as q:
            query: Query[CompaniesTableRow] = q.query(CompaniesTableRow)
            if company_id.type_of(CompanyId.Type.UUID):
                query = query.filter_by(id=company_id.type_of(CompanyId.Type.UUID).value)
            elif company_id.type_of(CompanyId.Type.JCN):
                query = query.filter_by(corporate_number=company_id.type_of(CompanyId.Type.JCN).value)
            optional = query.one_or_none()
            if optional is None:
                return None
            return optional.to_entity()

    def find_by_ids(self, *company_id: CompanyId) -> set[Company]:
        with self.__unit_of_work.query() as q:
            query: Query[CompaniesTableRow] = q.query(CompaniesTableRow)

            uuids = [id.type_of(CompanyId.Type.UUID).value for id in company_id if id.type_of(CompanyId.Type.UUID)]
            corporate_numbers = [id.type_of(CompanyId.Type.JCN).value for id in company_id if id.type_of(CompanyId.Type.JCN)]

            table_rows: list[CompaniesTableRow] = query.filter(or_(
                CompaniesTableRow.id.in_(uuids),
                CompaniesTableRow.corporate_number.in_(corporate_numbers),
            )).all()
            return set([tr.to_entity() for tr in table_rows])

    def find_one_by(self, **kwargs) -> Company | None:
        with self.__unit_of_work.query() as q:
            optional: CompaniesTableRow | None = q.query(CompaniesTableRow).filter_by(**kwargs).one_or_none()
            if optional is None:
                return None
            return optional.to_entity()

    def find_all_by(self, **kwargs) -> list[Company]:
        with self.__unit_of_work.query() as q:
            return [e.to_entity() for e in q.query(CompaniesTableRow).filter_by(**kwargs).all()]

    def upsert(self, company: Company) -> None:
        if self.find_by_id(company.id):
            self.update(company)
        else:
            self.insert(company)

    def insert(self, company: Company) -> None:
        self.__unit_of_work.persist(CompaniesTableRow.create(company))

    def update(self, company: Company) -> None:
        optional: CompaniesTableRow | None = self.__unit_of_work.session().query(CompaniesTableRow).get(company.id.value)
        if optional is None:
            raise Exception(f'{CompaniesTableRow.__tablename__}.{company.id.value} が存在しないため、更新できません。')

        self.__unit_of_work.delete(*optional.related_pages)
        self.__unit_of_work.delete(optional.summaries)
        self.__unit_of_work.delete(*optional.contact_points)
        self.__unit_of_work.delete(*optional.offices)
        self.__unit_of_work.flush()

        optional.update(company)

    def delete(self, company: Company) -> None:
        optional: CompaniesTableRow | None = self.__unit_of_work.session().query(CompaniesTableRow).get(company.id.value)
        if optional is None:
            return None

        self.__unit_of_work.delete(*optional.related_pages)
        self.__unit_of_work.delete(optional.summaries)
        self.__unit_of_work.delete(*optional.contact_points)
        self.__unit_of_work.delete(*optional.offices)
        self.__unit_of_work.flush()

        self.__unit_of_work.delete(optional)
