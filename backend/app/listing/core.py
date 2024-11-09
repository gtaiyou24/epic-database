from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener
from listing.domain.model.company import CompanyRepository
from listing.port.adapter.persistence.repository.inmem import InMemCompanyRepository
from listing.port.adapter.persistence.repository.mysql.company import MySQLCompanyRepository
from listing.port.adapter.resource.company import CompanyResource


class Listing(AppModule):
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
        router = APIRouter(tags=["Listing"])
        # router.include_router(DatasetResource().router)
        router.include_router(CompanyResource().router)
        return router

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return set()
