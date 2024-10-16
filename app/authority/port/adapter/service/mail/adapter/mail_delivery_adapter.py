import abc

from authority.domain.model.mail import Mail


class MailDeliveryAdapter(abc.ABC):
    @abc.abstractmethod
    def send(self, mail: Mail) -> None:
        pass
