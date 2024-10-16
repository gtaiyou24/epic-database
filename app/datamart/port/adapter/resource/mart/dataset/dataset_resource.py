from fastapi import APIRouter

from common.port.adapter.resource import APIResource
from datamart.port.adapter.resource.mart.dataset.response import DataJson


class DatasetResource(APIResource):
    router = APIRouter(prefix="/dataset")

    def __init__(self):
        self.router.add_api_route("", self.search, name="データ検索", response_model=list[DataJson])
        self.router.add_api_route("", self.create, name="データ作成", methods=["POST"], response_model=DataJson)
        self.router.add_api_route("/{data_id}", self.get, name="データ詳細詳細", response_model=DataJson)
        self.router.add_api_route("/{data_id}", self.update, name="データ更新", methods=["PUT"],
                                  response_model=DataJson)
        self.router.add_api_route("/{data_id}", self.patch, name="データ部分更新", methods=["PATCH"],
                                  response_model=DataJson)
        self.router.add_api_route("/{data_id}", self.delete, name="データ削除", methods=["DELETE"])

    def search(self, dataset_id: str):
        pass

    def create(self, dataset_id: str, request) -> DataJson:
        """新しいデータを新規作成"""
        pass

    def get(self, dataset_id: str, data_id: str) -> DataJson:
        pass

    def update(self, dataset_id: str, data_id: str, request) -> DataJson:
        """新しいデータに置き換える"""

    def patch(self, dataset_id: str, data_id: str, request) -> DataJson:
        """既存データに新しいプロパティを追加する"""
        pass

    def delete(self, dataset_id: str, data_id: str) -> None:
        pass
