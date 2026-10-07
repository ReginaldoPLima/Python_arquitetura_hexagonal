from pathlib import Path

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DATABASE"] = Path(__file__).with_name("enderecos.db")

    from app.presentation.routes import presentation
    from app.repository.endereco_repository import initialize_database

    with app.app_context():
        initialize_database()
    app.register_blueprint(presentation)
    return app