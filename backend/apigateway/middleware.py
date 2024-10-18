from __future__ import annotations

import time

from di import DIContainer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from apigateway.application.authentication import AuthenticationApplicationService


class MonitoringMiddleware(BaseHTTPMiddleware):
    """エラー / ログ監視を行うミドルウェア"""
    async def dispatch(self, request: Request, call_next):
        # TODO : Sentry / New Relic へエラー/ログを送信する
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        print(f"##### MonitoringMiddleware: process_time={process_time} #####")
        return response


class PublishInternalTokenMiddleware(BaseHTTPMiddleware):
    """アクセストークン、リフレッシュトークンなどの外部通信用トークンをもとに内部通信用トークンを発行するミドルウェア

    内部通信用トークンのペイロードについては、以下の資料を参照してください。
    * https://zenn.dev/mikakane/articles/tutorial_for_jwt
    * https://techblog.yahoo.co.jp/advent-calendar-2017/jwt/
    * https://qiita.com/KWS_0901/items/00446f9df1cdaadf36fc
    """
    http_bearer = HTTPBearer(auto_error=False)
    __authentication_application_service: AuthenticationApplicationService | None = None

    @property
    def authentication_application_service(self) -> AuthenticationApplicationService:
        self.__authentication_application_service = (
            self.__authentication_application_service or
            DIContainer.instance().resolve(AuthenticationApplicationService)
        )
        return self.__authentication_application_service

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        authorization: HTTPAuthorizationCredentials | None = await self.http_bearer(request)
        if authorization is None:
            return await call_next(request)

        dpo = self.authentication_application_service.publish_internal_token(authorization.credentials)
        jwt = dpo.add_audience(str(request.url)).generate_jwt()
        request.headers.__dict__["_list"].append((b'x-internal-token', jwt.encode()))
        response = await call_next(request)
        return response
