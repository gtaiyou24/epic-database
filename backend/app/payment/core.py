from typing import override

from di import DIContainer
from fastapi import APIRouter

from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener


class Payment(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(

        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["Payment"])
        return router

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return set()
