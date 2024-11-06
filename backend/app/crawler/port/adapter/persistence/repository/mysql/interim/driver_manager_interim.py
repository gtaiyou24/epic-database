from injector import inject

from common.application import UnitOfWork
from common.port.adapter.persistence.repository.mysql import MySQLUnitOfWork
from crawler.domain.model.interim import InterimId, Interim
from crawler.port.adapter.persistence.repository.mysql.interim.table import InterimsTableRow, InterimIdentityMapTableRow


class DriverManagerInterim:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_by_id(self, id: InterimId) -> Interim | None:
        with self.__unit_of_work.query() as q:
            if id.type_of(InterimId.Type.UUID):
                optional = q.query(InterimsTableRow).filter_by(id=id.type_of(InterimId.Type.UUID).value).one_or_none()
                if optional is None:
                    return None
                return optional.to_entity()

            optional = q.query(InterimIdentityMapTableRow)\
                .filter_by(value=id.value, type=id.type)\
                .one_or_none()

            if optional is None:
                return

            return optional.interim.to_entity()

    def find_one_by(self, **kwargs) -> Interim | None:
        with self.__unit_of_work.query() as q:
            optional: InterimsTableRow | None = q.query(InterimsTableRow).filter_by(**kwargs).one_or_none()
            if optional is None:
                return None
            return optional.to_entity()

    def find_all_by(self, **kwargs) -> list[Interim]:
        with self.__unit_of_work.query() as q:
            return [e.to_entity() for e in q.query(InterimsTableRow).filter_by(**kwargs).all()]

    def upsert(self, interim: Interim) -> None:
        if self.find_by_id(interim.id):
            self.update(interim)
        else:
            self.insert(interim)

    def insert(self, interim: Interim) -> None:
        self.__unit_of_work.persist(InterimsTableRow.create(interim))

    def update(self, interim: Interim) -> None:
        if interim.id.type_of(InterimId.Type.UUID):
            optional = self.__unit_of_work.session()\
                .query(InterimsTableRow)\
                .get(interim.id.type_of(InterimId.Type.UUID).value)\
                .one_or_none()

            if optional is None:
                raise Exception(f'{InterimsTableRow.__tablename__}.{interim.id.value} が存在しないため、更新できません。')
        else:
            identity = self.__unit_of_work.session()\
                .query(InterimIdentityMapTableRow)\
                .filter_by(value=interim.id.value, type=interim.id.type)\
                .one_or_none()

            if identity is None:
                raise Exception(f'{InterimsTableRow.__tablename__}.{interim.id.value} が存在しないため、更新できません。')

            optional = identity.interim

        self.__unit_of_work.delete(*optional.interim_identity_maps)
        self.__unit_of_work.flush()

        optional.update(interim)

    def delete(self, interim: Interim) -> None:
        if interim.id.type_of(InterimId.Type.UUID):
            optional = self.__unit_of_work.session() \
                .query(InterimsTableRow) \
                .get(interim.id.type_of(InterimId.Type.UUID).value) \
                .one_or_none()

            if optional is None:
                return None
        else:
            identity = self.__unit_of_work.session() \
                .query(InterimIdentityMapTableRow) \
                .filter_by(value=interim.id.value, type=interim.id.type) \
                .one_or_none()

            if identity is None:
                return None

            optional = identity.interim

        self.__unit_of_work.delete(*optional.interim_identity_maps)
        self.__unit_of_work.flush()

        self.__unit_of_work.delete(optional)
