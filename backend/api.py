import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slf4py import create_logger

from apigateway import apigateway
from authority import authority
from common import common
from listing import listing
from payment import payment
from apigateway.middleware import MonitoringMiddleware, PublishInternalTokenMiddleware
from common.exception import SystemException, ErrorCode
from common.port.adapter.resource.error import ErrorJson


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 起動前と終了後に実行する処理を記載する"""
    common.startup()
    apigateway.startup()
    authority.startup()
    listing.startup()
    payment.startup()
    yield
    common.shutdown()
    apigateway.shutdown()
    authority.shutdown()
    listing.startup()
    payment.shutdown()

app = FastAPI(
    title="Backend API",
    lifespan=lifespan,
    responses={
        422: {
            "model": ErrorJson,
            "description": "Unprocessable Entity",
            "content": {
                "application/json": {
                    "example": {
                        "type": "COMMON_2003",
                        "title": "無効なデータです",
                        "status": 422,
                        "instance": "https://localhost:8000/auth/token"
                    }
                }
            }
        }
    },
    root_path=os.getenv("OPENAPI_PREFIX"),
    # docs_url="/api/py/docs",
    # openapi_url="/api/py/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# app.add_middleware(HTTPSRedirectMiddleware)  # HTTPS を強制
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "example.com", "*.example.com"])  # ホストヘッダーを指定
app.add_middleware(MonitoringMiddleware)  # エラー/ログ監視のためのモニタリングを実行
app.add_middleware(PublishInternalTokenMiddleware)  # 内部通信用トークンを発行

app.include_router(apigateway.router)
app.include_router(authority.router)
app.include_router(market.router)
app.include_router(payment.router)
app.include_router(portfolio.router)


@app.exception_handler(SystemException)
async def system_exception_handler(request: Request, exception: SystemException) -> Response:
    exception.logging()
    return JSONResponse(
        status_code=exception.error_code.http_status,
        content=jsonable_encoder(
            {
                "type": exception.error_code.name,
                "title": exception.error_code.message,
                "status": exception.error_code.http_status,
                "instance": str(request.url),
            }
        ),
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, error: ValueError) -> Response:
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2002.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2002.name,
            "title": ErrorCode.COMMON_2002.message,
            "status": ErrorCode.COMMON_2002.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(AssertionError)
async def assertion_error_handler(request: Request, error: AssertionError) -> Response:
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2002.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2002.name,
            "title": ErrorCode.COMMON_2002.message,
            "status": ErrorCode.COMMON_2002.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, error: RequestValidationError) -> Response:
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2003.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2003.name,
            "title": ErrorCode.COMMON_2003.message,
            "status": ErrorCode.COMMON_2003.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, error: Exception) -> Response:
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_1000.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_1000.name,
            "title": ErrorCode.COMMON_1000.message,
            "status": ErrorCode.COMMON_1000.http_status,
            "instance": str(request.url)
        }),
    )
