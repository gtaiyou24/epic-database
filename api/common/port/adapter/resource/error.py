from http import HTTPStatus
from typing import Literal

from pydantic import BaseModel

from common.exception import ErrorCode


class ErrorJson(BaseModel):
    type: Literal[*[e.name for e in ErrorCode]]
    title: str
    status: HTTPStatus
    instance: str
