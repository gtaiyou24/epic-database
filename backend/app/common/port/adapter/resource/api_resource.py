import abc
from typing import Type

from di import DIContainer
from injector import T
from fastapi import APIRouter


class APIResource(abc.ABC):
    @property
    @abc.abstractmethod
    def router(self) -> APIRouter:
        pass

    def resolve(self, application_service: Type[T]) -> T:
        return DIContainer.instance().resolve(application_service)
