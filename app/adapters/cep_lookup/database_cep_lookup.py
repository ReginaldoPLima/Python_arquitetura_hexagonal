from app.domain.ports.cep_lookup import CepLookupPort
from app.domain.ports.endereco_repository import EnderecoRepositoryPort


class DatabaseCepLookup(CepLookupPort):
    def __init__(self, repository: EnderecoRepositoryPort):
        self.repository = repository

    def buscar_por_cep(self, cep: str) -> dict[str, str] | None:
        return self.repository.buscar_por_cep(cep)