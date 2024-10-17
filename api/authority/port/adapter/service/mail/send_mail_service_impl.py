from injector import inject
from typing import override

from authority.domain.model.mail import SendMailService, Mail
from authority.port.adapter.service.mail.adapter import MailDeliveryAdapter


class SendMailServiceImpl(SendMailService):
    @inject
    def __init__(self, mail_delivery_adapter: MailDeliveryAdapter):
        self.__mail_delivery_adapter = mail_delivery_adapter

    @override
    def send(self, mail: Mail) -> None:
        self.__mail_delivery_adapter.send(mail)
