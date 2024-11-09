from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener
from crawler.domain.model.page import PageService
from crawler.domain.model.listing import ListingManagementService
from crawler.domain.model.interim import InterimRepository
from crawler.port.adapter.messaging import DownloadGBizINFOListener, TransferCompanyListener, ScrapeCompanyListener
from crawler.port.adapter.persistence.repository.inmem import InMemInterimRepository
from crawler.port.adapter.persistence.repository.mysql.interim import MySQLInterimRepository
from crawler.port.adapter.service.page import PageServiceImpl
from crawler.port.adapter.service.page.adapter import SearchEngineAdapter
from crawler.port.adapter.service.page.adapter.google import GoogleAdapter
from crawler.port.adapter.service.page.adapter.stub import SearchEngineAdapterStub
from crawler.port.adapter.service.listing import ListingManagementServiceImpl
from crawler.port.adapter.service.listing.adapter import ListingAdapter
from crawler.port.adapter.service.listing.adapter.module import ListingModuleAdapter
from crawler.port.adapter.service.listing.adapter.stub import ListingAdapterStub


class Crawler(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            # Repository
            DI.of(InterimRepository, {"InMem": InMemInterimRepository}, MySQLInterimRepository),

            # Service
            DI.of(ListingManagementService, {}, ListingManagementServiceImpl),
            DI.of(PageService, {}, PageServiceImpl),

            # Adapter
            DI.of(ListingAdapter, {"Stub": ListingAdapterStub}, ListingModuleAdapter),
            DI.of(SearchEngineAdapter, {"Stub": SearchEngineAdapterStub}, GoogleAdapter),
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        raise NotImplementedError(f"{self.__class__.__name__}モジュールにはAPI Routerがありません。")

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return {
            DownloadGBizINFOListener(),
            ScrapeCompanyListener(),
            TransferCompanyListener(),
        }
