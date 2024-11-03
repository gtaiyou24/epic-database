from fastapi import APIRouter
from fastapi.params import Depends

from common.port.adapter.resource import APIResource
from common.port.adapter.resource.dependency import AuthenticateAdminUser
from listing.port.adapter.resource.dataset.response import CompanyJson


class CompanyResource(APIResource):
    router = APIRouter(prefix="/companies")

    def __init__(self):
        self.router.add_api_route("", self.search, name="企業データ検索", response_model=list[CompanyJson])
        self.router.add_api_route("", self.create, name="企業データ作成", methods=["POST"], response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.get, name="企業データ詳細詳細", response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.update, name="企業データ更新", methods=["PUT"], response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.patch, name="企業データ部分更新", methods=["PATCH"],
                                  response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.delete, name="企業データ削除", methods=["DELETE"])

    def search(self, name: str):
        pass

    def create(self, name: str, request, _ = Depends(AuthenticateAdminUser())) -> CompanyJson:
        """新しいデータを新規作成"""
        pass

    def get(self, id: str) -> CompanyJson:
        pass

    def update(self, name: str, id: str, request, _ = Depends(AuthenticateAdminUser())) -> CompanyJson:
        """新しいデータに置き換える"""

    def patch(self, name: str, id: str, request, _ = Depends(AuthenticateAdminUser())) -> CompanyJson:
        """既存データに新しいプロパティを追加する"""
        pass

    def delete(self, name: str, id: str, _ = Depends(AuthenticateAdminUser())) -> None:
        pass
