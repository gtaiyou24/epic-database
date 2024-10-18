import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html2text import html2text

from authority.domain.model.mail import Mail
from authority.port.adapter.service.mail.adapter import MailDeliveryAdapter


class GmailAdapter(MailDeliveryAdapter):
    def send(self, mail: Mail) -> None:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(mail.from_.text, os.getenv('GMAIL_SMTP_PASSWORD'))

            mime = MIMEMultipart("alternative")
            mime["Subject"] = mail.subject
            mime["From"] = mail.from_.text
            mime["To"] = mail.to.text

            mime.attach(MIMEText(html2text(mail.html), "plain"))
            mime.attach(MIMEText(mail.html, "html"))

            smtp.sendmail(mail.from_.text, mail.to.text, mime.as_string())
