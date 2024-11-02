from typing import override, Self

from slf4py import set_logger

from common.domain.model import DomainEvent
from common.event import EventStore, EventSerializer, StoredEvent


@set_logger
class InMemEventStore(EventStore):
    def __init__(self):
        self.__stored_events: list[StoredEvent] = []
        self.__event_serializer = EventSerializer()

    @override
    def all_stored_events_between(self, from_stored_event_id: int, to_stored_event_id: int) -> list[StoredEvent]:
        if len(self.__stored_events) == 0:
            return []
        return self.__stored_events[from_stored_event_id:to_stored_event_id + 1]

    @override
    def all_stored_events_since(self, stored_event_id: int) -> list[StoredEvent]:
        return self.all_stored_events_between(stored_event_id, len(self.__stored_events))

    @override
    def append(self, domain_event: DomainEvent) -> Self:
        self.log.debug("ドメインイベント {} を追加します".format(domain_event))
        stored_event = StoredEvent.new(len(self.__stored_events) + 1, domain_event)
        self.__stored_events.append(stored_event)
        self.log.debug("ストアドイベントの件数 {}".format(len(self.__stored_events)))
        return self
