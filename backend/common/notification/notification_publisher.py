import abc


class NotificationPublisher(abc.ABC):
    @abc.abstractmethod
    def publish_notifications(self) -> None:
        pass
