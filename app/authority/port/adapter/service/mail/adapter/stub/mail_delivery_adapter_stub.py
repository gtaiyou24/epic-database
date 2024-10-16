from authority.domain.model.mail import Mail
from authority.port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailDeliveryAdapterStub(MailDeliveryAdapter):
    def send(self, mail: Mail) -> None:
        print(f'send "{mail.subject}" to {mail.to.text}')
