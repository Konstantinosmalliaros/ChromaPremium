import os

from dotenv import load_dotenv
from flask import Flask


load_dotenv()


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory for the Chroma Premium site."""

    app = Flask(__name__, instance_relative_config=False)

    from .config import Config

    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    from .routes import main

    app.register_blueprint(main)

    @app.context_processor
    def inject_year() -> dict[str, int]:
        from datetime import date

        return {"current_year": date.today().year}

    return app

