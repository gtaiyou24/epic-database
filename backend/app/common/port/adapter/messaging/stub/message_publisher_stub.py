from typing import override

from common.notification import Notification
from common.port.adapter.messaging import MessagePublisher


class MessagePublisherStub(MessagePublisher):
    def __init__(self):
        self.__messages: dict[str, list[Notification]] = {}

    @override
    def publish(self, notification: Notification) -> None:
        message_list = self.__messages.get(notification.type_name, [])
        message_list.append(notification)
        self.__messages[notification.type_name] = message_list
