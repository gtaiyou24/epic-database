from __future__ import annotations

import abc
from typing import Self

from common.domain.model import DomainEvent
from common.event import StoredEvent


class EventStore(abc.ABC):
    @abc.abstractmethod
    def all_stored_events_between(self, from_stored_event_id: int, to_stored_event_id: int) -> list[StoredEvent]:
        pass

    @abc.abstractmethod
    def all_stored_events_since(self, stored_event_id: int) -> list[StoredEvent]:
        pass

    @abc.abstractmethod
    def append(self, domain_event: DomainEvent) -> Self:
        pass
