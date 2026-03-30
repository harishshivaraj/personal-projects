from __future__ import annotations

import smtplib
from email.message import EmailMessage


def send_email_alert(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    from_address: str,
    to_address: str,
    subject: str,
    body: str,
) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_address
    message["To"] = to_address
    message.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)
