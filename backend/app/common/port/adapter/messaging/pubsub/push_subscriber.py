import base64
import json

from fastapi import HTTPException
from slf4py import set_logger
from fastapi.requests import Request

from common.port.adapter.messaging import ExchangeListener


@set_logger
class PushSubscriber:
    """Push サブスクリプション

    https://cloud.google.com/pubsub/docs/push?hl=ja
    """
    def __init__(self, subscribers: set[ExchangeListener]):
        self._subscribers = subscribers

    async def receive(self, request: Request) -> None:
        envelope = await request.json()
        if not envelope:
            msg = "no Pub/Sub message received"
            self.log.error(f"error: {msg}")
            raise HTTPException(status_code=400, detail=f"Bad Request: {msg}")

        if not isinstance(envelope, dict) or "message" not in envelope:
            msg = f"invalid Pub/Sub message format: {envelope}"
            self.log.error(f"error: {msg}")
            raise HTTPException(status_code=400, detail=msg)

        pubsub_message = envelope["message"]
        if not isinstance(pubsub_message, dict) or "data" not in pubsub_message:
            msg = f"invalid Pub/Sub message format: {pubsub_message}"
            self.log.error(f"error: {msg}")
            raise HTTPException(status_code=400, detail=msg)

        try:
            data = json.loads(base64.b64decode(pubsub_message["data"]).decode())
        except Exception as e:
            self.log.error(e)
            raise HTTPException(status_code=400,
                                detail="Invalid Pub/Sub message: data property is not valid base64 encoded JSON")

        publisher_name = data.get("publisher_name")
        event_type = data.get("event_type")
        for subscriber in self._subscribers:
            if subscriber.publisher_name() == publisher_name and subscriber.listens_to(event_type):
                subscriber.filtered_dispatch(event_type, base64.b64decode(pubsub_message["data"]).decode())
