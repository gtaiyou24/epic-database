from fastapi import APIRouter

from common.port.adapter.resource import APIResource
from datamart.port.adapter.resource.mart.dataset import DatasetResource


class MartResource(APIResource):
    router = APIRouter(prefix="/mart")

    def __init__(self):
        self.router.add_api_route("", self.list, name="データセット一覧取得")
        self.router.include_router(DatasetResource().router, prefix="/{dataset_id}")

    def list(self):
        pass
