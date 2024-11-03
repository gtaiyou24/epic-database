from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener
from dataset.domain.model.company import CompanyRepository
from dataset.port.adapter.persistence.repository.inmem import InMemCompanyRepository
from dataset.port.adapter.persistence.repository.mysql.company import MySQLCompanyRepository
from dataset.port.adapter.resource.company import CompanyResource


class DataSet(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            DI.of(CompanyRepository, {"InMem": InMemCompanyRepository}, MySQLCompanyRepository),
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["DataSet"])
        # router.include_router(DatasetResource().router)
        router.include_router(CompanyResource().router)
        return router

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return set()