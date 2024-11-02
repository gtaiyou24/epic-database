from injector import inject, singleton

from common.event import EventStore
from common.notification import NotificationPublisher, PublishedNotificationTrackerStore, Notification
from common.port.adapter.messaging import MessagePublisher


@singleton
class NotificationPublisherImpl(NotificationPublisher):
    @inject
    def __init__(self,
                 published_notification_tracker_store: PublishedNotificationTrackerStore,
                 event_store: EventStore,
                 message_publisher: MessagePublisher):
        self.__published_notification_tracker_store = published_notification_tracker_store
        self.__event_store = event_store
        self.__message_publisher = message_publisher

    def publish_notifications(self) -> None:
        """
        1. PublishedNotificationTrackerを取得する
        2. 直近発行されたNotificationのID指定で「未発行のNotification」を取得する
        3. MQに発行する
        4. 発行状況を記録する
        """
        published_notification_tracker = self.__published_notification_tracker_store.published_notification_tracker()

        notifications = self.__list_unpublished_notifications(
            published_notification_tracker.most_recent_published_notification_id)

        try:
            for notification in notifications:
                self.__message_publisher.publish(notification)

            self.__published_notification_tracker_store.track_most_recent_published_notification(
                published_notification_tracker, notifications)
        except Exception as e:
            print("NotificationPublisher problem: " + str(e))

    def __list_unpublished_notifications(self, most_recent_published_notification_id: int) -> list[Notification]:
        """未発行なすべてのNotificationのインスタンスを並び替え、そのリストを取得する"""
        notifications = list()
        for stored_event in self.__event_store.all_stored_events_since(most_recent_published_notification_id):
            domain_event = stored_event.to_domain_event()
            notifications.append(Notification(stored_event.event_id, domain_event))
        return notifications
