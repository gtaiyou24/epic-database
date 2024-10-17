from typing import override

from di import DIContainer
from fastapi import APIRouter

from common.core import AppModule
from datamart.port.adapter.resource.mart import MartResource


class DataMart(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register()

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["Data Mart"])
        router.include_router(MartResource().router)
        return router
