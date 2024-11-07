from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import VARCHAR, DateTime, func, Index, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.port.adapter.persistence.repository.mysql import DataBase
from crawler.domain.model.interim import Interim, InterimId
from crawler.domain.model.url import URLSet


class InterimIdentityMapTableRow(DataBase):
    __tablename__ = 'interim_identity_maps'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'id')),
        (Index(f'idx_{__tablename__}_2', 'type')),
        (Index(f'idx_{__tablename__}_3', 'id', 'type')),
        (UniqueConstraint('value', 'type', name=f"uix_{__tablename__}_1")),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="ID")
    value: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="中間データの識別子")
    type: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="中間データの識別タイプ")
    interim_id: Mapped[str] = mapped_column(
        ForeignKey('interims.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    interim: Mapped[InterimsTableRow] = relationship(
        "InterimsTableRow",
        back_populates="interim_identity_maps"
    )

    @staticmethod
    def create(interim_payload: Interim) -> list[InterimIdentityMapTableRow]:
        uuid = interim_payload.id.type_of(InterimId.Type.UUID)
        return [
            InterimIdentityMapTableRow(
                value=id.value,
                type=id.type.name,
                interim_id=uuid.value
            ) for id in interim_payload.id
        ]

    def to_value(self) -> InterimId:
        return InterimId.Type[self.type].make(self.value)


class InterimsTableRow(DataBase):
    __tablename__ = 'interims'
    __table_args__ = (
        (Index(f'idx_{__tablename__}_1', 'id')),
        (Index(f'idx_{__tablename__}_2', 'source')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, nullable=False, comment="UUID")
    source: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="スクレイピング元の種類")
    payload: Mapped[str] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),
                                                 onupdate=func.now())

    interim_identity_maps: Mapped[list[InterimIdentityMapTableRow]] = relationship(back_populates="interim",
                                                                                   lazy='joined')

    @staticmethod
    def create(interim: Interim) -> InterimsTableRow:
        uuid = interim.id.type_of(InterimId.Type.UUID)
        return InterimsTableRow(
            id=uuid.value,
            source=interim.source.name,
            payload=json.dumps(interim.payload),
            interim_identity_maps=InterimIdentityMapTableRow.create(interim)
        )

    def update(self, interim: Interim) -> None:
        self.source = interim.source.name
        self.payload = json.dumps(interim.payload)

    def to_entity(self) -> Interim:
        id = InterimId.Type.UUID.make(self.id)
        for other_id in self.interim_identity_maps:
            other_id = other_id.to_value()
            if id.contains(other_id.type):
                continue
            id = id.set_other_id(other_id)
        return Interim(
            id=id,
            source=Interim.Source[self.source],
            from_urls=URLSet(set()),
            payload=json.loads(self.payload),
        )
