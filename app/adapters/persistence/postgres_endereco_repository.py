import psycopg
from psycopg.rows import dict_row

from app.adapters.persistence.demo_data import enderecos_de_demonstracao
from app.domain.errors import CepDuplicadoError
from app.domain.ports.endereco_repository import EnderecoRepositoryPort


class PostgresEnderecoRepository(EnderecoRepositoryPort):
    def __init__(self, database_url: str):
        self.database_url = database_url

    def initialize(self) -> None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS enderecos (
                    cep VARCHAR(8) PRIMARY KEY CHECK(char_length(cep) = 8),
                    logradouro TEXT NOT NULL,
                    bairro TEXT NOT NULL,
                    cidade TEXT NOT NULL,
                    uf CHAR(2) NOT NULL CHECK(char_length(uf) = 2)
                )
                """
            )
            count = connection.execute("SELECT COUNT(*) AS total FROM enderecos").fetchone()["total"]
            if count == 0:
                with connection.cursor() as cursor:
                    cursor.executemany(
                        """
                        INSERT INTO enderecos (cep, logradouro, bairro, cidade, uf)
                        VALUES (%(cep)s, %(logradouro)s, %(bairro)s, %(cidade)s, %(uf)s)
                        """,
                        enderecos_de_demonstracao(),
                    )

    def listar_todos(self) -> list[dict[str, str]]:
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            rows = connection.execute("SELECT * FROM enderecos ORDER BY cep").fetchall()
            return [dict(row) for row in rows]

    def buscar_por_cep(self, cep: str) -> dict[str, str] | None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "SELECT * FROM enderecos WHERE cep = %s", (cep,)
            ).fetchone()
            return dict(row) if row else None

    def salvar(self, endereco: dict[str, str]) -> None:
        try:
            with psycopg.connect(self.database_url) as connection:
                connection.execute(
                    """
                    INSERT INTO enderecos (cep, logradouro, bairro, cidade, uf)
                    VALUES (%(cep)s, %(logradouro)s, %(bairro)s, %(cidade)s, %(uf)s)
                    """,
                    endereco,
                )
        except psycopg.errors.UniqueViolation as error:
            raise CepDuplicadoError from error