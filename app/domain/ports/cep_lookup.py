from abc import ABC, abstractmethod


class CepLookupPort(ABC):
    @abstractmethod
    def buscar_por_cep(self, cep: str) -> dict[str, str] | None:
        raise NotImplementedError