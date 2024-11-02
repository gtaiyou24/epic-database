import abc

from common.notification import PublishedNotificationTracker, Notification


class PublishedNotificationTrackerStore(abc.ABC):
    def published_notification_tracker(self) -> PublishedNotificationTracker:
        return self.published_notification_tracker_of(self.type_name())

    @abc.abstractmethod
    def published_notification_tracker_of(self, type_name: str) -> PublishedNotificationTracker:
        pass

    @abc.abstractmethod
    def track_most_recent_published_notification(self,
                                                 published_notification_tracker: PublishedNotificationTracker,
                                                 notifications: list[Notification]):
        pass

    @abc.abstractmethod
    def type_name(self) -> str:
        pass
