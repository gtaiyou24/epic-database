from __future__ import annotations

from functools import wraps
from typing import override, Callable

from di import DIContainer
from injector import singleton, inject

from common.application import UnitOfWork
from common.domain.model import DomainEventSubscriber, DomainEvent, DomainEventPublisher
from common.event import EventStore
from common.notification import NotificationPublisher


class DomainEventSubscriberImpl(DomainEventSubscriber[DomainEvent]):
    def __init__(self, event_store: EventStore):
        self.__event_store = event_store

    @override
    def subscribed_to_event_type(self) -> type[DomainEvent]:
        return DomainEvent

    @override
    def handle_event(self, domain_event: DomainEvent):
        self.__event_store.append(domain_event)


@singleton
class ApplicationServiceLifeCycle:
    @inject
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 event_store: EventStore):
        self.__is_listening = True
        self.__unit_of_work = unit_of_work
        self.__event_store = event_store
        self.__notification_application_service = DIContainer.instance().resolve(NotificationApplicationService)

    def begin(self, is_listening: bool = True) -> None:
        self.__is_listening = is_listening
        if self.__is_listening:
            self.listen()
        self.__unit_of_work.start()

    def fail(self, exception: Exception | None = None) -> None:
        self.__unit_of_work.rollback()
        if exception is not None:
            raise exception

    def success(self) -> None:
        self.__unit_of_work.commit()
        # TODO : コミット時に通知を発行するのではなく、別スレッドで発行するようにする
        if self.__is_listening is True:
            self.__notification_application_service.publish_notifications()

    def listen(self):
        DomainEventPublisher.instance().reset()
        DomainEventPublisher.instance().subscribe(DomainEventSubscriberImpl(self.__event_store))


def transactional[T](method: Callable[..., T] | None = None, is_listening: bool = True):
    def _transactional[T](method: Callable[..., T]):
        """AOPによるトランザクション管理を行うためのデコーダー"""
        @wraps(method)
        def handle_transaction(*args, **kwargs) -> T:
            application_life_cycle = DIContainer.instance().resolve(ApplicationServiceLifeCycle)

            application_life_cycle.begin(is_listening)
            try:
                _return = method(*args, **kwargs)
                application_life_cycle.success()
                return _return
            except Exception as e:
                application_life_cycle.fail(e)

        return handle_transaction

    # @transactional もしくは @transactional() で呼び出したとき
    if method is None:
        return _transactional

    return _transactional(method)


# NOTE : 循環参照エラーを防ぐためにこちらに定義
@singleton
class NotificationApplicationService:
    @inject
    def __init__(self, notification_publisher: NotificationPublisher):
        self.__notification_publisher = notification_publisher

    @transactional(is_listening=False)
    def publish_notifications(self) -> None:
        self.__notification_publisher.publish_notifications()
