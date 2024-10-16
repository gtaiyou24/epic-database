from di import DIContainer
from fastapi import APIRouter
from fastapi.params import Depends

from authority.application.identity import IdentityApplicationService
from authority.application.identity.command import UnlinkAccountCommand, LinkAccountCommand
from authority.port.adapter.resource.user.account.request import LinkAccountRequest, UnlinkAccountRequest
from common.port.adapter.resource import APIResource
from dependency import CurrentUser, GetCurrentUser


class AccountResource(APIResource):
    router = APIRouter(prefix="/users/account")

    def __init__(self):
        self.__identity_application_service: IdentityApplicationService | None = None
        self.router.add_api_route("/", self.link, methods=["POST"], name="アカウント連携")
        self.router.add_api_route("/", self.unlink, methods=["DELETE"], name='アカウント連携解除')

    @property
    def identity_application_service(self) -> IdentityApplicationService:
        self.__identity_application_service = (
            self.__identity_application_service or DIContainer.instance().resolve(IdentityApplicationService)
        )
        return self.__identity_application_service

    def link(self,
             request: LinkAccountRequest,
             current_user: CurrentUser = Depends(GetCurrentUser({"ALL"}))) -> None:
        command = LinkAccountCommand(
            user_id=current_user.id,
            provider=request.provider,
            code=request.code,
            redirect_uri=request.redirect_uri,
            code_verifier=request.code_verifier,
            grant_type=request.grant_type
        )
        self.identity_application_service.link(command)

    def unlink(self, request: UnlinkAccountRequest, current_user: CurrentUser = Depends(GetCurrentUser({"ALL"}))) -> None:
        command = UnlinkAccountCommand(current_user.id, request.provider)
        self.identity_application_service.unlink(command)