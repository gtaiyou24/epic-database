from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ContactPoint:
    class Type(Enum):
        """問い合わせ用途"""
        TELEPHONE = 'telephone'
        EMAIL = 'email'
        FAX = 'fax'
        FORM = 'form'

        @staticmethod
        def value_of(value: str) -> ContactPoint.Type:
            for type in ContactPoint.Type:
                if value == type.value:
                    return type
            raise ValueError(f'Invalid contact point type: {value}')

        def make(self, value: str) -> ContactPoint:
            return ContactPoint(self, value)

    type: Type
    value: str
