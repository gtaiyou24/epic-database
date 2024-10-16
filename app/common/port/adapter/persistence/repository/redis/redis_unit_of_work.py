from typing import override

from injector import singleton, inject
from redis.client import Pipeline, StrictRedis

from common.application import UnitOfWork
from common.port.adapter.persistence.repository.redis import KeyValue


@singleton
class RedisUnitOfWork(UnitOfWork[KeyValue]):
    @inject
    def __init__(self, client: StrictRedis):
        self.__pipeline: Pipeline | None = None
        self.__client = client

    @override
    def mark(self, instance: KeyValue) -> None:
        pass

    @override
    def persist(self, instance: KeyValue) -> None:
        # 現状、データ型が少なく、ロジックも複雑ではないため、if 文で実装しています。
        # ですが、保存ロジックが複雑になってきたら別クラスに切り出したりすること。
        if instance.type == KeyValue.Type.STRING:
            self.__pipeline.set(instance.key, instance.value, ex=instance.ttl_seconds, nx=True)  # 上書き不可
        else:
            raise NotImplementedError("現状、String 型しか対応していません。")

    @override
    def delete(self, *instances: KeyValue) -> None:
        self.__pipeline.delete(*[e.key for e in instances])

    @override
    def start(self) -> None:
        if self.__pipeline is None:
            # 本来、Redis Pipeline は multi/exec 間で1回の CRUD 処理を飛ばすのでラウンドトリップが少なくなり、
            # パフォーマンスが上がるというものですが、便宜的にトランザクションっぽい動きになるように利用します。
            self.__pipeline = self.__client.pipeline()
            self.__pipeline.multi()
        # すでにトランザクションが開始されている場合は何もしない

    @override
    def flush(self) -> None:
        pass

    @override
    def rollback(self) -> None:
        self.__pipeline.discard()
        self.__pipeline.reset()
        self.__pipeline = None

    @override
    def commit(self) -> None:
        if self.__pipeline is None:
            raise SystemError("Redis トランザクションが実行されていないため、コミットできません。")
        self.__pipeline.execute()
        self.__pipeline.reset()
