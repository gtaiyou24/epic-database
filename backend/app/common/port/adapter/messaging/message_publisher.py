import abc

from common.notification import Notification


class MessagePublisher(abc.ABC):
    @abc.abstractmethod
    def publish(self, notification: Notification) -> None:
        pass
