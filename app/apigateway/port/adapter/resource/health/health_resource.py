from typing import override

from fastapi import APIRouter

from common.port.adapter.resource import APIResource


class HealthResource(APIResource):
    def __init__(self):
        self.__router = APIRouter(prefix="/health")
        self.__router.add_api_route(
            "/check", self.check, methods=["GET"],
            responses={
                200: {
                    "content": {
                        "application/json": {
                            "example": {"health": True}
                        }
                    }
                }
            },
            name="ヘルスチェック",
            description="リクエスト可能な状態かを確認できます。"
        )

    @override
    @property
    def router(self) -> APIRouter:
        return self.__router

    def check(self) -> dict:
        return {"health": True}
