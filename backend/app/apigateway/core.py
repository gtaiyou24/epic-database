from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from apigateway.domain.model.secret import SecretManagerService
from apigateway.domain.model.user import IdentityAccessService
from apigateway.port.adapter.messaging import HealthCheckListener
from apigateway.port.adapter.resource.health import HealthResource
from apigateway.port.adapter.service.secret import SecretManagerServiceImpl
from apigateway.port.adapter.service.secret.adapter import SecretManagerAdapter
from apigateway.port.adapter.service.secret.adapter.stub import SecretManagerAdapterStub
from apigateway.port.adapter.service.user import IdentityAccessServiceImpl
from apigateway.port.adapter.service.user.adapter import AuthorityAdapter, IdentityAccessAdapter
from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener


class ApiGateway(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            # Service
            DI.of(SecretManagerService, {}, SecretManagerServiceImpl),
            DI.of(IdentityAccessService, {}, IdentityAccessServiceImpl),
            # Adapter
            DI.of(SecretManagerAdapter, {}, SecretManagerAdapterStub),
            DI.of(IdentityAccessAdapter, {}, AuthorityAdapter)
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["API Gateway"])
        router.include_router(HealthResource().router)
        return router

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return {HealthCheckListener()}
