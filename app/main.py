import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apigateway import apigateway
from common import common
from common.port.adapter.resource.error import ErrorJson
from apigateway.middleware import MonitoringMiddleware, PublishInternalTokenMiddleware
from datamart import datamart


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 起動前と終了後に実行する処理を記載する"""
    common.startup()
    apigateway.startup()
    datamart.startup()
    yield
    common.shutdown()
    apigateway.shutdown()
    datamart.shutdown()


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
                        "instance": "https://localhost:8000/health/check"
                    }
                }
            }
        }
    },
    root_path=os.getenv("OPENAPI_PREFIX")
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
app.include_router(datamart.router)
