import datetime
import json
from typing import override

import pytz

from apigateway.domain.model.token import BearerToken, AccessToken
from apigateway.domain.model.user import UserId
from common.port.adapter.persistence.repository.redis import KeyValue


class TokenKeyValue(KeyValue[BearerToken]):
    @staticmethod
    @override
    def create(entity: BearerToken) -> KeyValue:
        tz = pytz.timezone('Asia/Tokyo')
        return TokenKeyValue(
            KeyValue.Type.STRING,
            entity.value,
            json.dumps({
                'type': entity.type.name,
                'user_id': entity.user_id.value,
                'value': entity.value,
                'published_at': entity.published_at.strftime('%Y-%m-%d %H:%M:%S'),
                'expires_at': entity.expires_at.strftime('%Y-%m-%d %H:%M:%S'),
                'pair_token': entity.pair_token
            }),
            ttl_seconds=(entity.expires_at - datetime.datetime.now().astimezone(tz)).seconds
        )

    @staticmethod
    @override
    def from_(payload: str) -> KeyValue:
        payload: dict = json.loads(payload)
        tz = pytz.timezone('Asia/Tokyo')

        expires_at = datetime.datetime.strptime(payload['expires_at'], '%Y-%m-%d %H:%M:%S')
        return TokenKeyValue(
            KeyValue.Type.STRING,
            payload['value'],
            payload,
            (expires_at.astimezone(tz) - datetime.datetime.now().astimezone(tz)).seconds
        )

    @override
    def to_entity(self) -> BearerToken:
        tz = pytz.timezone('Asia/Tokyo')
        return BearerToken.Type[self.value['type']].make(
            UserId(self.value['user_id']),
            self.value['value'],
            datetime.datetime.strptime(self.value['published_at'], '%Y-%m-%d %H:%M:%S').astimezone(tz),
            datetime.datetime.strptime(self.value['expires_at'], '%Y-%m-%d %H:%M:%S').astimezone(tz),
            self.value['pair_token']
        )
