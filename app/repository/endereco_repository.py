import sqlite3
from contextlib import contextmanager

from flask import current_app


class CepDuplicadoError(Exception):
    pass


@contextmanager
def _connection():
    connection = sqlite3.connect(current_app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    with _connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS enderecos (
                cep TEXT PRIMARY KEY CHECK(length(cep) = 8),
                logradouro TEXT NOT NULL,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                uf TEXT NOT NULL CHECK(length(uf) = 2)
            )
            """
        )
        if connection.execute("SELECT COUNT(*) FROM enderecos").fetchone()[0] == 0:
            bairros = ["Centro", "Jardim das Flores", "Vila Nova", "Parque Central", "Boa Vista"]
            connection.executemany(
                """
                INSERT INTO enderecos (cep, logradouro, bairro, cidade, uf)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        f"01001{index:03d}",
                        f"Rua de Demonstracao {index + 1}",
                        bairros[index % len(bairros)],
                        "Cidade Exemplo",
                        "SP",
                    )
                    for index in range(50)
                ],
            )


def listar_todos() -> list[sqlite3.Row]:
    with _connection() as connection:
        return connection.execute("SELECT * FROM enderecos ORDER BY cep").fetchall()


def buscar_por_cep(cep: str) -> sqlite3.Row | None:
    with _connection() as connection:
        return connection.execute(
            "SELECT * FROM enderecos WHERE cep = ?", (cep,)
        ).fetchone()


def salvar(endereco: dict[str, str]) -> None:
    try:
        with _connection() as connection:
            connection.execute(
                """
                INSERT INTO enderecos (cep, logradouro, bairro, cidade, uf)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    endereco["cep"],
                    endereco["logradouro"],
                    endereco["bairro"],
                    endereco["cidade"],
                    endereco["uf"],
                ),
            )
    except sqlite3.IntegrityError as error:
        raise CepDuplicadoError from error