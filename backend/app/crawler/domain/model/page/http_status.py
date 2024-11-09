from __future__ import annotations

from enum import Enum


class HttpStatus(Enum):
    UNKNOWN = 0
    OK = 200
    BAD_REQUEST = 400
    UNAUTHRORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

    @staticmethod
    def value_of(status: int) -> HttpStatus:
        for e in HttpStatus:
            if e.value == status:
                return e
        return HttpStatus.UNKNOWN
