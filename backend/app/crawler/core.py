from typing import override

from fastapi import APIRouter

from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener
from crawler.port.adapter.messaging import DownloadGBizINFOListener


class Crawler(AppModule):
    @override
    def startup(self) -> None:
        pass

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
            DownloadGBizINFOListener()
        }
