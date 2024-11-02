from __future__ import annotations

import base64
import pickle

from common.domain.model import DomainEvent


class EventSerializer:
    def serialize(self, domain_event: DomainEvent) -> str:
        return base64.b64encode(pickle.dumps(domain_event)).decode("utf-8")

    def deserialize(self, payload: str) -> DomainEvent:
        return pickle.loads(base64.b64decode(payload.encode()))
