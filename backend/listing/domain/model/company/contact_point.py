import abc
from enum import Enum


class ContactPoint(abc.ABC):
    class Type(Enum):
        """問い合わせ用途"""
        TELEPHONE = 'telephone'
        EMAIL = 'email'
        FAX = 'fax'
        FORM = 'form'

    type: Type


class Telephone(ContactPoint):
    number: str


class Email(ContactPoint):
    address: str


class Fax(ContactPoint):
    number: str

class Form(ContactPoint):
    url: str
