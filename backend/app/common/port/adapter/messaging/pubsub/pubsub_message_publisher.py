from typing import override

from google.cloud.pubsub_v1 import PublisherClient
from slf4py import set_logger

from common.notification import Notification, NotificationSerializer
from common.port.adapter.messaging import MessagePublisher


@set_logger
class PubSubMessagePublisher(MessagePublisher):
    """Google の Pub/Sub にメッセージを送信するクラス"""
    def __init__(self, project_id: str, topic_id: str):
        self.__project_id = project_id
        self.__topic_id = topic_id
        self.__notification_serializer = NotificationSerializer("toushire")
        self.__publisher = PublisherClient()

    @override
    def publish(self, notification: Notification) -> None:
        serialized_notification: str = self.__notification_serializer.serialize(notification)
        future = self.__publisher.publish(
            self.__publisher.topic_path(self.__project_id, self.__topic_id),
            serialized_notification.encode('utf-8')
        )
        message_id = future.result(timeout=300)
        self.log.debug(f"Published {serialized_notification.encode('utf-8')} to {self.__topic_id} : {message_id}")
