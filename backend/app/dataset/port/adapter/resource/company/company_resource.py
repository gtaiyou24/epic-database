from di import DIContainer
from fastapi import APIRouter
from fastapi.params import Depends

from common.port.adapter.resource import APIResource
from common.port.adapter.resource.dependency import AuthenticateAdminUser
from dataset.application.company import CompanyApplicationService
from dataset.application.company.command import SaveCompanyCommand
from dataset.port.adapter.resource.company.json import CompanyJson


class CompanyResource(APIResource):
    router = APIRouter(prefix="/companies")

    def __init__(self):
        self.__company_application_service = None
        self.router.add_api_route("", self.search, name="企業データ検索", response_model=list[CompanyJson])
        self.router.add_api_route("", self.save, name="企業データ作成", methods=["POST"], response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.get, name="企業データ詳細詳細", response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.save, name="企業データ更新", methods=["PUT"], response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.patch, name="企業データ部分更新", methods=["PATCH"],
                                  response_model=CompanyJson)
        self.router.add_api_route("/{id}", self.delete, name="企業データ削除", methods=["DELETE"])

    @property
    def company_application_service(self) -> CompanyApplicationService:
        self.__company_application_service = (
            self.__company_application_service or DIContainer.instance().resolve(CompanyApplicationService)
        )
        return self.__company_application_service

    def search(self, name: str):
        pass

    def save(self, request: CompanyJson, _ = Depends(AuthenticateAdminUser())) -> CompanyJson:
        """新しいデータを新規作成"""
        command = SaveCompanyCommand(
            uuid=request.uuid,
            corporate_number=request.jcn,
            name=request.name,
            description=request.description,
            founded_at=request.founded_at,
            homepage=request.homepage,
            same_as=request.same_as,
            summaries=request.summaries,
            contact_points=[dict(point) for point in request.contact_points],
            offices=request.offices,
        )
        dpo = self.company_application_service.save(command)
        return CompanyJson.from_(dpo)

    def get(self, id: str) -> CompanyJson:
        dpo = self.company_application_service.company_with_id(id)
        return CompanyJson.from_(dpo)

    def patch(self, name: str, id: str, request, _ = Depends(AuthenticateAdminUser())) -> CompanyJson:
        """既存データに新しいプロパティを追加する"""
        pass

    def delete(self, name: str, id: str, _ = Depends(AuthenticateAdminUser())) -> None:
        pass
