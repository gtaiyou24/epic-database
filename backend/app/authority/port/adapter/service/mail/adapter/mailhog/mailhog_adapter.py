import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html2text import html2text

from authority.domain.model.mail import Mail
from authority.port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailHogAdapter(MailDeliveryAdapter):
    def __init__(self):
        self.__smtp = smtplib.SMTP(host="mailhog", port=1025)

    def send(self, mail: Mail) -> None:
        mine = MIMEMultipart("alternative")
        mine["Subject"] = mail.subject
        mine["From"] = mail.from_.text
        mine["To"] = mail.to.text

        mine.attach(MIMEText(html2text(mail.html), "plain"))
        mine.attach(MIMEText(mail.html, "html"))

        self.__smtp.sendmail(mail.from_.text, mail.to.text, mine.as_string())
