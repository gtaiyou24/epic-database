from di import DIContainer
from fastapi import APIRouter, Depends

from authority.application.authorization import AuthorizationApplicationService
from authority.application.authorization.command import AuthenticateAccountCommand
from authority.port.adapter.resource.auth.google.request import AuthorizationCodeForm
from authority.port.adapter.resource.auth.response import TokenJson
from common.port.adapter.resource import APIResource


class GoogleResource(APIResource):
    router = APIRouter(prefix="/auth/google")

    def __init__(self):
        self.__authorization_application_service: AuthorizationApplicationService | None = None
        self.router.add_api_route("/token", self.token, methods=["POST"], response_model=TokenJson, name="Google 認証")

    @property
    def authorization_application_service(self) -> AuthorizationApplicationService:
        self.__authorization_application_service = (
            self.__authorization_application_service or DIContainer.instance().resolve(AuthorizationApplicationService)
        )
        return self.__authorization_application_service

    def token(self, form: AuthorizationCodeForm = Depends()) -> TokenJson:
        command = AuthenticateAccountCommand(
            provider='GOOGLE',
            code=form.code,
            redirect_uri=form.redirect_uri,
            code_verifier=form.code_verifier,
            grant_type=form.grant_type
        )
        dpo = self.authorization_application_service.authenticate_with_account(command)
        return TokenJson.from_(dpo)
