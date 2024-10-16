from typing import override

from fastapi import APIRouter

from common.core import AppModule


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
