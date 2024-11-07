from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener
from crawler.domain.model.dataset import DatasetService
from crawler.domain.model.interim import InterimRepository
from crawler.port.adapter.messaging import DownloadGBizINFOListener, TransferCompanyListener
from crawler.port.adapter.persistence.repository.inmem import InMemInterimRepository
from crawler.port.adapter.persistence.repository.mysql.interim import MySQLInterimRepository
from crawler.port.adapter.service.dataset import DatasetServiceImpl
from crawler.port.adapter.service.dataset.adapter import DatasetAdapter
from crawler.port.adapter.service.dataset.adapter.dataset import DatasetModuleAdapter
from crawler.port.adapter.service.dataset.adapter.stub import DatasetAdapterStub


class Crawler(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            # Repository
            DI.of(InterimRepository, {"InMem": InMemInterimRepository}, MySQLInterimRepository),

            # Service
            DI.of(DatasetService, {}, DatasetServiceImpl),

            # Adapter
            DI.of(DatasetAdapter, {"Stub": DatasetAdapterStub}, DatasetModuleAdapter),
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
            TransferCompanyListener(),
        }
