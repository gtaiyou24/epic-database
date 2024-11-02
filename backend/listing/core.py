from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener
from listing.domain.model.company import CompanyRepository
from listing.port.adapter.persistence.repository.inmem import InMemCompanyRepository
from listing.port.adapter.persistence.repository.mysql.company import MySQLCompanyRepository
from listing.port.adapter.resource.mart import MartResource


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
        router = APIRouter(tags=["Data Mart"])
        router.include_router(MartResource().router)
        return router

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return set()