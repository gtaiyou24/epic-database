from authority.domain.model.mail import Mail
from authority.port.adapter.service.mail.adapter import MailDeliveryAdapter


class SendGridAdapter(MailDeliveryAdapter):
    """https://sendgrid.kke.co.jp/"""

    def send(self, mail: Mail) -> None:
        raise NotImplementedError()
