from abc import ABC, abstractmethod


class EnderecoRepositoryPort(ABC):
    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> list[dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_cep(self, cep: str) -> dict[str, str] | None:
        raise NotImplementedError

    @abstractmethod
    def salvar(self, endereco: dict[str, str]) -> None:
        raise NotImplementedError