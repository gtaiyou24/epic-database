import json

from common.notification import Notification


class NotificationSerializer:
    def __init__(self, publisher_name: str):
        self.__publisher_name = publisher_name

    def serialize(self, notification: Notification) -> str:
        notification_dict = notification.__dict__()
        notification_dict['publisher_name'] = self.__publisher_name
        return json.dumps(notification_dict)
