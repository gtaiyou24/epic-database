from contextlib import contextmanager
from typing import override

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from common.application import UnitOfWork
from common.port.adapter.persistence.repository.mysql import DataBase
from common.port.adapter.persistence.repository.redis import RedisUnitOfWork


class MySQLUnitOfWork(UnitOfWork[DataBase]):
    @inject
    def __init__(self, engine: Engine, redis_unit_of_work: RedisUnitOfWork):
        self.__engine = engine
        self.__redis_unit_of_work = redis_unit_of_work
        self.__ThreadLocalSession = scoped_session(sessionmaker(
            bind=self.__engine,
            autocommit=False,
            expire_on_commit=True
        ))

    @contextmanager
    def query(self) -> Session:
        """
        SELECTクエリを発行する用のセッションを発行する。
        トランザクション管理対象ではないデータの取得にはこのメソッドを利用してください。
        トランザクション管理の対象となるデータ更新・新規作成・削除・更新のためのデータ取得は self.session() を利用してください。
        """
        session = Session(bind=self.__engine)
        try:
            yield session
        finally:
            session.close()

    def session(self) -> Session:
        """トランザクション管理をするためにスレッドローカルのセッションを発行する"""
        return self.__ThreadLocalSession()

    @override
    def mark(self, instance: DataBase) -> None:
        """UnitOfWorkの追跡対象に追加

        self.mark() に指定されたインスタンスは self.persist() にて、更新するインスタンスか新規作成するインスタンスかどうかの判定に用いる。
        """
        pass

    @override
    def persist(self, instance: DataBase) -> None:
        """永続化対象としてインスタンスを追跡する"""
        # NOTE : INSERT もしくは UPDATE されるオブジェクトを指定
        self.session().add(instance)

    @override
    def delete(self, *instances: DataBase) -> None:
        """削除対象としてオブジェクトを追跡する"""
        for instance in instances:
            self.session().delete(instance)

    @override
    def start(self) -> None:
        if self.session().in_transaction():
            return
            # MEMO: モジュラーを跨いだトランザクションが発生することを考慮し、以下の制御はコメントアウトしました。

            # すでに何かしらのトランザクションが開始されている場合は、前回のセッションを削除し、新しいセッションを作成する
            # self.__ThreadLocalSession.remove()
            # self.__ThreadLocalSession.close()
        self.session().begin()
        self.__redis_unit_of_work.start()

    @override
    def flush(self) -> None:
        self.session().flush()
        self.__redis_unit_of_work.flush()

    @override
    def rollback(self) -> None:
        self.session().rollback()
        self.__ThreadLocalSession.remove()
        self.__ThreadLocalSession.close()
        self.__redis_unit_of_work.rollback()

    @override
    def commit(self) -> None:
        self.session().commit()
        self.__ThreadLocalSession.remove()
        self.__ThreadLocalSession.close()
        self.__redis_unit_of_work.commit()
