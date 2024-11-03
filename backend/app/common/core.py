import abc
import os
from typing import override

from di import DIContainer, DI
from fastapi import APIRouter
from redis import StrictRedis
from sqlalchemy import create_engine, Engine

from common.application import UnitOfWork
from common.event import EventStore
from common.notification import PublishedNotificationTrackerStore, NotificationPublisher
from common.port.adapter.messaging import ExchangeListener, MessagePublisher
from common.port.adapter.messaging.stub import MessagePublisherStub
from common.port.adapter.notification.notification_publisher_impl import NotificationPublisherImpl
from common.port.adapter.persistence.event.inmem import InMemEventStore
from common.port.adapter.persistence.notification.inmem import InMemPublishedNotificationTrackerStore
from common.port.adapter.persistence.repository.inmem import InMemUnitOfWork
from common.port.adapter.persistence.repository.mysql import MySQLUnitOfWork, DataBase
from common.port.adapter.persistence.repository.redis import RedisUnitOfWork


class AppModule(abc.ABC):
    """各モジュールでDI設定やルーティングなどを定義させるためのクラス"""
    @abc.abstractmethod
    def startup(self) -> None:
        """アプリ起動前に実行すべき処理を定義する"""
        pass

    @abc.abstractmethod
    def shutdown(self) -> None:
        """アプリ終了時に実行すべき処理をを定義する"""
        pass

    @property
    @abc.abstractmethod
    def router(self) -> APIRouter:
        """ルーティングを定義"""
        pass

    @property
    @abc.abstractmethod
    def subscribers(self) -> set[ExchangeListener]:
        """サブスクライバーを定義"""
        pass


class Common(AppModule):
    @override
    def startup(self) -> None:
        if "InMem" not in os.getenv("DI_PROFILE_ACTIVES", []):
            # データベースを構築する
            engine = create_engine(os.getenv("DATABASE_URL"), echo=os.getenv("SLF4PY_LOG_LEVEL", "DEBUG") == "DEBUG")
            DIContainer.instance().register(DI.of(Engine, {}, engine))
            DataBase.metadata.create_all(bind=engine)

        DIContainer.instance().register(
            DI.of(UnitOfWork, {"InMem": InMemUnitOfWork}, MySQLUnitOfWork),
            DI.of(RedisUnitOfWork, {}, RedisUnitOfWork),
            DI.of(StrictRedis, {}, StrictRedis(
                host=os.getenv('REDIS_HOST'),
                port=os.getenv('REDIS_PORT'),
                db=0,
                protocol=3,  # PESP3
                decode_responses=True)),
            DI.of(EventStore, {"InMem": InMemEventStore}, InMemEventStore),
            DI.of(NotificationPublisher, {}, NotificationPublisherImpl),
            DI.of(PublishedNotificationTrackerStore,
                  {"InMem": InMemPublishedNotificationTrackerStore},
                  InMemPublishedNotificationTrackerStore),
            DI.of(MessagePublisher,
                  {"Stub": MessagePublisherStub},
                  InMemPublishedNotificationTrackerStore),
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        raise NotImplementedError("CommonモジュールにはAPI Routerがありません。")

    @override
    @property
    def subscribers(self) -> set[ExchangeListener]:
        return set()
