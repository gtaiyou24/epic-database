from __future__ import annotations

import datetime
from dataclasses import dataclass

from common.domain.model import DomainEvent
from common.event import EventSerializer


@dataclass(init=False)
class StoredEvent:
    event_id: int
    type_name: str
    event_body: str
    occurred_on: datetime.datetime

    def __init__(self, event_id: int, type_name: str, event_body: str, occurred_on: datetime.datetime):
        super().__setattr__("event_id", event_id)
        super().__setattr__("type_name", type_name)
        super().__setattr__("event_body", event_body)
        super().__setattr__("occurred_on", occurred_on)

    @staticmethod
    def new(event_id: int, domain_event: DomainEvent) -> StoredEvent:
        payload = EventSerializer().serialize(domain_event)
        return StoredEvent(event_id, domain_event.type_name(), payload, domain_event.occurred_on)

    def to_domain_event(self) -> DomainEvent:
        return EventSerializer().deserialize(self.event_body)

    def __hash__(self):
        return self.event_id + (1237 * 233)
