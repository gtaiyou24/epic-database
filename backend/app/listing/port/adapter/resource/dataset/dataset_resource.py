from fastapi import APIRouter

from common.port.adapter.resource import APIResource
from listing.port.adapter.resource.dataset.response import DataJson


class DatasetResource(APIResource):
    router = APIRouter(prefix="/dataset")

    def __init__(self):
        self.router.add_api_route("", self.search, name="データ検索", response_model=list[DataJson])
        self.router.add_api_route("", self.create, name="データ作成", methods=["POST"], response_model=DataJson)
        self.router.add_api_route("/{id}", self.get, name="データ詳細詳細", response_model=DataJson)
        self.router.add_api_route("/{id}", self.update, name="データ更新", methods=["PUT"], response_model=DataJson)
        self.router.add_api_route("/{id}", self.patch, name="データ部分更新", methods=["PATCH"],
                                  response_model=DataJson)
        self.router.add_api_route("/{id}", self.delete, name="データ削除", methods=["DELETE"])

    def search(self, name: str):
        pass

    def create(self, name: str, request) -> DataJson:
        """新しいデータを新規作成"""
        pass

    def get(self, name: str, id: str) -> DataJson:
        return DataJson({'first': "taiyo", "last": "tamura"})

    def update(self, name: str, id: str, request) -> DataJson:
        """新しいデータに置き換える"""

    def patch(self, name: str, id: str, request) -> DataJson:
        """既存データに新しいプロパティを追加する"""
        pass

    def delete(self, name: str, id: str) -> None:
        pass
