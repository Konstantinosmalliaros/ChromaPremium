from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import Any

from flask import current_app


class EmailConfigurationError(RuntimeError):
    """Raised when SMTP configuration is incomplete."""


def send_contact_email(form_data: dict[str, Any]) -> None:
    """Send a contact email using the configured SMTP settings."""

    app = current_app
    config = app.config

    required_settings = (
        "SMTP_SERVER",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
    )

    if not all(config.get(setting) for setting in required_settings):
        raise EmailConfigurationError(
            "SMTP configuration is incomplete. Set SMTP_SERVER, SMTP_PORT, "
            "SMTP_USERNAME, and SMTP_PASSWORD environment variables."
        )

    message = EmailMessage()
    message["Subject"] = "Νέο μήνυμα από την φόρμα επικοινωνίας"
    message["From"] = config.get("SMTP_USERNAME")
    message["To"] = config.get("CONTACT_RECIPIENT")

    body_lines = [
        "Λάβατε ένα νέο μήνυμα από την φόρμα επικοινωνίας του Chroma Premium.",
        "",
        f"Όνομα: {form_data.get('name', '')}",
        f"Email: {form_data.get('email', '')}",
        f"Τηλέφωνο: {form_data.get('phone', '–')}",
        "",
        "Μήνυμα:",
        form_data.get("message", ""),
    ]

    message.set_content("\n".join(body_lines))

    use_ssl = config.get("SMTP_USE_SSL", False)

    if use_ssl:
        server_class = smtplib.SMTP_SSL
    else:
        server_class = smtplib.SMTP

    with server_class(config["SMTP_SERVER"], config["SMTP_PORT"]) as server:
        if not use_ssl and config.get("SMTP_USE_TLS", True):
            server.starttls()

        server.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
        server.send_message(message)

