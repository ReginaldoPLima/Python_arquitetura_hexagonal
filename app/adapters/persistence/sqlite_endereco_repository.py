import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.adapters.persistence.demo_data import enderecos_de_demonstracao
from app.domain.errors import CepDuplicadoError
from app.domain.ports.endereco_repository import EnderecoRepositoryPort


class SQLiteEnderecoRepository(EnderecoRepositoryPort):
    def __init__(self, database_path: Path):
        self.database_path = database_path

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self._connection() as connection:
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
                connection.executemany(
                    """
                    INSERT INTO enderecos (cep, logradouro, bairro, cidade, uf)
                    VALUES (:cep, :logradouro, :bairro, :cidade, :uf)
                    """,
                    enderecos_de_demonstracao(),
                )

    def listar_todos(self) -> list[dict[str, str]]:
        with self._connection() as connection:
            rows = connection.execute("SELECT * FROM enderecos ORDER BY cep").fetchall()
            return [dict(row) for row in rows]

    def buscar_por_cep(self, cep: str) -> dict[str, str] | None:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM enderecos WHERE cep = ?", (cep,)
            ).fetchone()
            return dict(row) if row else None

    def salvar(self, endereco: dict[str, str]) -> None:
        try:
            with self._connection() as connection:
                connection.execute(
                    """
                    INSERT INTO enderecos (cep, logradouro, bairro, cidade, uf)
                    VALUES (:cep, :logradouro, :bairro, :cidade, :uf)
                    """,
                    endereco,
                )
        except sqlite3.IntegrityError as error:
            raise CepDuplicadoError from error