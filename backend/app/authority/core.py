import os
from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from authority.domain.model.mail import SendMailService
from authority.domain.model.token import TokenRepository
from authority.domain.model.user import EncryptionService, UserRepository
from authority.domain.model.user.account import OAuthProviderService
from authority.port.adapter.persistence.repository.inmem import InMemUserRepository, InMemTokenRepository
from authority.port.adapter.persistence.repository.mysql.user import MySQLUserRepository
from authority.port.adapter.persistence.repository.redis.token import RedisTokenRepository
from authority.port.adapter.resource.auth.auth_resource import AuthResource
from authority.port.adapter.resource.auth.google import GoogleResource
from authority.port.adapter.resource.user import UserResource
from authority.port.adapter.resource.user.account.account_resource import AccountResource
from authority.port.adapter.service.mail import SendMailServiceImpl
from authority.port.adapter.service.mail.adapter import MailDeliveryAdapter
from authority.port.adapter.service.mail.adapter.gmail import GmailAdapter
from authority.port.adapter.service.mail.adapter.mailhog import MailHogAdapter
from authority.port.adapter.service.mail.adapter.sendgrid import SendGridAdapter
from authority.port.adapter.service.mail.adapter.stub import MailDeliveryAdapterStub
from authority.port.adapter.service.user import EncryptionServiceImpl
from authority.port.adapter.service.user.account import OAuthProviderServiceImpl
from authority.port.adapter.service.user.account.adapter import GoogleAdapter
from common.core import AppModule
from common.port.adapter.messaging import ExchangeListener


class Authority(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            # Persistence
            DI.of(TokenRepository, {"InMem": InMemTokenRepository}, RedisTokenRepository),
            DI.of(UserRepository, {"InMem": InMemUserRepository}, MySQLUserRepository),
            # Service
            DI.of(SendMailService, {}, SendMailServiceImpl),
            DI.of(OAuthProviderService, {}, OAuthProviderServiceImpl),
            DI.of(EncryptionService, {}, EncryptionServiceImpl),
            # Adapter
            DI.of(
                GoogleAdapter,
                {},
                GoogleAdapter(os.getenv('GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_SECRET'))
            ),
            DI.of(
                MailDeliveryAdapter,
                {"SendGrid": SendGridAdapter, "MailHog": MailHogAdapter, "Gmail": GmailAdapter},
                MailDeliveryAdapterStub
            ),
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["Authority"])
        router.include_router(AuthResource().router)
        router.include_router(GoogleResource().router)
        router.include_router(UserResource().router)
        router.include_router(AccountResource().router)
        return router

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return set()
