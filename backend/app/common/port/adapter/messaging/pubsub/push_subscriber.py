import base64
import json

from fastapi import HTTPException
from slf4py import set_logger
from fastapi.requests import Request

from common.port.adapter.messaging import ExchangeListener
from common.port.adapter.messaging.pubsub.json import MessageJson


@set_logger
class PushSubscriber:
    """Push サブスクリプション

    https://cloud.google.com/pubsub/docs/push?hl=ja
    """
    def __init__(self, subscribers: set[ExchangeListener]):
        self._subscribers = subscribers

    async def receive(self, request: MessageJson) -> None:
        try:
            plain_json = base64.b64decode(request.message.data).decode()
            data = json.loads(plain_json)
        except Exception as e:
            self.log.error(e)
            raise HTTPException(status_code=400,
                                detail="Invalid Pub/Sub message: data property is not valid base64 encoded JSON")

        publisher_name = data.get("publisher_name")
        event_type = data.get("event_type")
        for subscriber in self._subscribers:
            if subscriber.publisher_name() == publisher_name and subscriber.listens_to(event_type):
                subscriber.filtered_dispatch(event_type, plain_json)
