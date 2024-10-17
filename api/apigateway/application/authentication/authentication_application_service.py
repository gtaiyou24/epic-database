from injector import singleton, inject

from apigateway.application.authentication.dpo import InternalTokenDpo
from apigateway.domain.model.secret import SecretManagerService, Key
from apigateway.domain.model.token.internal import InternalToken
from apigateway.domain.model.user import IdentityAccessService
from common.exception import SystemException, ErrorCode


@singleton
class AuthenticationApplicationService:
    @inject
    def __init__(self,
                 identity_access_service: IdentityAccessService,
                 secret_manager_service: SecretManagerService):
        self.identity_access_service = identity_access_service
        self.secret_manager_service = secret_manager_service

    def publish_internal_token(self, access_token_value: str) -> InternalTokenDpo:
        user = self.identity_access_service.authenticate(access_token_value)

        if user is None:
            raise SystemException(ErrorCode.INVALID_TOKEN, f"アクセストークン {access_token_value} は無効です。")

        private_key = self.secret_manager_service.get(Key.JWT_PRIVATE)
        return InternalTokenDpo(InternalToken.generate(user), private_key)
