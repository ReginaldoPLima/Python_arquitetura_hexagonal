import os
from pathlib import Path

from flask import Flask

from app.adapters.cep_lookup.correios_cep_lookup import CorreiosCepLookup
from app.adapters.cep_lookup.database_cep_lookup import DatabaseCepLookup
from app.adapters.persistence.sqlite_endereco_repository import SQLiteEnderecoRepository
from app.domain.ports.cep_lookup import CepLookupPort
from app.domain.ports.endereco_repository import EnderecoRepositoryPort
from app.service.endereco_service import EnderecoService


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE_ADAPTER=os.getenv("DATABASE_ADAPTER", "sqlite").lower(),

        SQLITE_DATABASE_PATH=os.getenv(
            "SQLITE_DATABASE_PATH", str(Path(__file__).with_name("enderecos.db"))
        ),

        DATABASE_URL=os.getenv("DATABASE_URL", ""),

        CEP_LOOKUP_ADAPTER=os.getenv("CEP_LOOKUP_ADAPTER", "database").lower(),

        CORREIOS_API_URL=os.getenv(
            "CORREIOS_API_URL", "https://api.correios.com.br/cep/v1/enderecos"
        ),
        
        CORREIOS_API_TOKEN=os.getenv("CORREIOS_API_TOKEN", ""),
    )
    if config:
        app.config.update(config)

    repository: EnderecoRepositoryPort

    if app.config["DATABASE_ADAPTER"] == "sqlite":
        repository = SQLiteEnderecoRepository(Path(app.config["SQLITE_DATABASE_PATH"]))



    elif app.config["DATABASE_ADAPTER"] == "postgres":

        from app.adapters.persistence.postgres_endereco_repository import PostgresEnderecoRepository

        database_url = app.config["DATABASE_URL"]
        if not database_url:
            raise ValueError("Defina DATABASE_URL para usar o PostgreSQL.")
        repository = PostgresEnderecoRepository(database_url)
    else:
        raise ValueError("DATABASE_ADAPTER deve ser 'sqlite' ou 'postgres'.")

    repository.initialize()

    cep_lookup: CepLookupPort


    if app.config["CEP_LOOKUP_ADAPTER"] == "database":
        cep_lookup = DatabaseCepLookup(repository)


    elif app.config["CEP_LOOKUP_ADAPTER"] == "correios":
        token = app.config["CORREIOS_API_TOKEN"]
        if not token:
            raise ValueError("Defina CORREIOS_API_TOKEN para usar a API dos Correios.")
        cep_lookup = CorreiosCepLookup(app.config["CORREIOS_API_URL"], token)

    else:
        raise ValueError("CEP_LOOKUP_ADAPTER deve ser 'database' ou 'correios'.")

    from app.presentation.routes import presentation

    app.extensions["endereco_service"] = EnderecoService(repository, cep_lookup)
    app.register_blueprint(presentation)
    return app