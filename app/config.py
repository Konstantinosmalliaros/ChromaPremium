import os


class Config:
    """Base configuration for the Chroma Premium website."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    CONTACT_RECIPIENT = os.environ.get("CONTACT_RECIPIENT", "info@chromapremium.gr")

    SMTP_SERVER = os.environ.get("SMTP_SERVER")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
    SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"
    SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "false").lower() == "true"

