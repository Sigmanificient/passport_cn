import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def send_mail(to_address: str, subject: str, body: str, port: int = 587) -> None:
    msg: MIMEMultipart = MIMEMultipart("alternative")

    msg["Subject"]: str = subject
    msg["From"]: str = config.smtp_user
    msg["To"]: str = to_address
    msg["Cc"]: str = config.smtp_user

    msg.attach(MIMEText(body, "html"))
    s: smtplib.SMTP = smtplib.SMTP(config.smtp_server, port)
    # s.connect(server, port)

    s.ehlo()
    s.starttls()

    # s.ehlo()
    s.login(config.smtp_user, config.smtp_password)
    s.sendmail(config.smtp_user, to_address, msg.as_string())
    s.quit()
