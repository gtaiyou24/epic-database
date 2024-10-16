from __future__ import annotations

import abc
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Self


@dataclass(init=False, unsafe_hash=True, frozen=True)
class DomainEvent(abc.ABC):
    """ドメインイベント"""
    event_version: int
    occurred_on: datetime

    def __init__(self, event_version: int, occurred_on: datetime):
        super().__setattr__("event_version", event_version)
        super().__setattr__("occurred_on", occurred_on)

    def type_name(self) -> str:
        return f'{self.__class__.__name__}.{self.event_version}'

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """MQのペイロードとして送信するJSON形式の値を指定"""
        pass


class DomainEventPublisher(threading.local):
    """パブリッシャー"""
    __instance: DomainEventPublisher | None = None

    def __init__(self):
        self.__subscribers: set[DomainEventSubscriber] = set()

    @classmethod
    def instance(cls) -> DomainEventPublisher:
        if cls.__instance:
            return cls.__instance

        cls.__instance = DomainEventPublisher()
        return cls.__instance

    def reset(self) -> Self:
        self.__subscribers = set()
        return self

    def publish(self, domain_event: DomainEvent) -> None:
        for subscriber in self.__subscribers:
            # サブスクライブするクラスタイプを取得し、型をチェックする
            if isinstance(domain_event, subscriber.subscribed_to_event_type()):
                subscriber.handle_event(domain_event)

    def subscribe(self, subscriber: DomainEventSubscriber) -> None:
        self.__subscribers.add(subscriber)


class DomainEventSubscriber[T](abc.ABC):
    """サブスクライバー"""

    @abc.abstractmethod
    def handle_event(self, domain_event: T) -> None:
        pass

    @abc.abstractmethod
    def subscribed_to_event_type(self) -> type[T]:
        pass
