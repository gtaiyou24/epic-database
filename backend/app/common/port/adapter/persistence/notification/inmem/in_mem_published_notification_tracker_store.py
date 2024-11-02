from common.notification import PublishedNotificationTrackerStore, PublishedNotificationTracker, Notification


class InMemPublishedNotificationTrackerStore(PublishedNotificationTrackerStore):
    __trackers: dict[str, PublishedNotificationTracker] = dict()

    def __init__(self):
        self.__type_name = "toushire"

    def published_notification_tracker_of(self, type_name: str) -> PublishedNotificationTracker:
        return self.__trackers.get(self.type_name(), PublishedNotificationTracker.new(type_name))

    def track_most_recent_published_notification(self,
                                                 published_notification_tracker: PublishedNotificationTracker,
                                                 notifications: list[Notification]):
        published_notification_tracker.update(notifications)
        self.__trackers[self.type_name()] = published_notification_tracker

    def type_name(self) -> str:
        return self.__type_name
