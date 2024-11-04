from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette import status
from starlette.requests import Request

from apigateway import apigateway
from authority import authority
from common import common
from common.port.adapter.messaging.pubsub import PushSubscriber
from common.port.adapter.messaging.pubsub.json import MessageJson
from common.port.adapter.resource.error import ErrorJson
from crawler import crawler
from dataset import dataset
from payment import payment


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 起動前と終了後に実行する処理を記載する"""
    common.startup()
    apigateway.startup()
    authority.startup()
    crawler.startup()
    dataset.startup()
    payment.startup()
    yield
    common.shutdown()
    apigateway.shutdown()
    authority.shutdown()
    crawler.shutdown()
    dataset.shutdown()
    payment.shutdown()


app = FastAPI(
    title="Subscriber",
    description="Google Pub/Sub や AWS SNS などのメッセージングシステムから POST されたメッセージを処理する Push 型サブスクリプション",
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
    }
)


@app.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def receive(request: MessageJson):
    """Receive and parse Pub/Sub messages."""
    all_subscribers = set()
    for module in [common, apigateway, authority, crawler, dataset, payment]:
        for subscriber in module.subscribers:
            all_subscribers.add(subscriber)

    push_subscriber = PushSubscriber(all_subscribers)
    await push_subscriber.receive(request)
