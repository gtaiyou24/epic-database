from typing import override

from injector import inject
from redis import StrictRedis

from apigateway.domain.model.token import TokenRepository, BearerToken
from apigateway.port.adapter.persistence.repository.redis.token import TokenKeyValue
from common.port.adapter.persistence.repository.redis import RedisUnitOfWork


class RedisTokenRepository(TokenRepository):
    @inject
    def __init__(self, redis_unit_of_work: RedisUnitOfWork, redis_client: StrictRedis):
        self.__redis_unit_of_work = redis_unit_of_work
        self.__redis_client = redis_client

    @override
    def add(self, token: BearerToken) -> None:
        self.__redis_unit_of_work.persist(TokenKeyValue.create(token))

    @override
    def remove(self, *token: BearerToken) -> None:
        for e in token:
            self.__redis_unit_of_work.delete(TokenKeyValue.create(e))

    @override
    def token_with_value(self, value: str) -> BearerToken | None:
        payload: str | None = self.__redis_client.get(value)
        if payload is None:
            return None
        return TokenKeyValue.from_(payload).to_entity()
