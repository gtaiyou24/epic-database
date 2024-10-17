from fastapi import APIRouter

from common.port.adapter.resource import APIResource
from datamart.port.adapter.resource.mart.dataset.response import DataJson, CompanyJson


class CompanyResource(APIResource):
    router = APIRouter(prefix="/dataset")

    def __init__(self):
        self.router.add_api_route("", self.search, name="データ検索", response_model=list[CompanyJson])
        self.router.add_api_route("", self.create, name="データ作成", methods=["POST"], response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.get, name="データ詳細詳細", response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.update, name="データ更新", methods=["PUT"], response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.patch, name="データ部分更新", methods=["PATCH"],
                                  response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.delete, name="データ削除", methods=["DELETE"])

    def search(self, name: str):
        pass

    def create(self, name: str, request) -> DataJson:
        """新しいデータを新規作成"""
        pass

    def get(self, id: str) -> CompanyJson:
        pass

    def update(self, name: str, id: str, request) -> DataJson:
        """新しいデータに置き換える"""

    def patch(self, name: str, id: str, request) -> DataJson:
        """既存データに新しいプロパティを追加する"""
        pass

    def delete(self, name: str, id: str) -> None:
        pass
