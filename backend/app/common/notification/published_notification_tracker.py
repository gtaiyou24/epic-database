from __future__ import annotations

from dataclasses import dataclass

from common.notification import Notification


@dataclass(init=False, unsafe_hash=True)
class PublishedNotificationTracker:
    """
    どのイベントが発行済みであるかの記録を永続化するもの

    parameters:
     - tracker_id: このオブジェクトの一意な識別子
     - type_name: イベントの発行先のトピック/チャネルの型についての説明
     - most_recent_published_notification_id:
       StoredEventとしてシリアライズして永続化された、特定のDomainEventの一意な識別子を保持する。つまり、この属性が保持するのは、直近に
       発行されたインスタンスのStoredEventのevent_idである。
    """
    tracker_id: int
    type_name: str
    most_recent_published_notification_id: int

    def __init__(self, tracker_id: int, type_name: str, most_recent_published_notification_id: int):
        assert isinstance(tracker_id, int), "tracker_idにはint型を指定してください。"
        assert isinstance(type_name, str), "type_nameにはstr型を指定してください。"
        assert isinstance(most_recent_published_notification_id, int), "「直近に発行された通知のID」にはint型を指定してください。"
        super().__setattr__("tracker_id", tracker_id)
        super().__setattr__("type_name", type_name)
        super().__setattr__("most_recent_published_notification_id", most_recent_published_notification_id)

    @staticmethod
    def new(type_name: str) -> PublishedNotificationTracker:
        return PublishedNotificationTracker(0, type_name, 0)

    def update(self, notifications: list[Notification]):
        if len(notifications) != 0:
            self.most_recent_published_notification_id = notifications[-1].notification_id
