import datetime
from dataclasses import dataclass

from common.domain.model import DomainEvent


@dataclass(init=False, eq=False)
class Notification:
    notification_id: int
    event: DomainEvent
    occurred_on: datetime.datetime
    type_name: str
    version: int

    def __init__(self, notification_id: int, event: DomainEvent):
        super().__setattr__("notification_id", notification_id)
        super().__setattr__("event", event)
        super().__setattr__("occurred_on", event.occurred_on)
        super().__setattr__("type_name", event.type_name())
        super().__setattr__("version", event.event_version)

    def __eq__(self, other):
        if not isinstance(other, Notification):
            return False
        return other.notification_id == self.notification_id

    def __hash__(self):
        return (3017 * 197) + self.notification_id

    def __dict__(self) -> dict:
        """シリアライズする際に利用"""
        return {
            'notification_id': self.notification_id,
            'event': self.event.to_dict(),
            'occurred_on': self.occurred_on.strftime('%Y-%m-%d %H:%M:%S'),
            'event_type': self.type_name,
            'version': self.version,
        }
