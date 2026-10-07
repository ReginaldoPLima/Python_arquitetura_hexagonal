import re
from typing import Any

from app.domain.errors import CepDuplicadoError
from app.domain.ports.cep_lookup import CepLookupPort
from app.domain.ports.endereco_repository import EnderecoRepositoryPort


def _normalizar_cep(value: str) -> str | None:
    cep = re.sub(r"\D", "", value)
    return cep if len(cep) == 8 else None


def _formatar_endereco(endereco: dict[str, str]) -> dict[str, str]:
    formatted = dict(endereco)
    formatted["cep"] = f"{formatted['cep'][:5]}-{formatted['cep'][5:]}"
    return formatted


class EnderecoService:
    def __init__(
        self,
        repository: EnderecoRepositoryPort,
        cep_lookup: CepLookupPort,
    ):
        self.repository = repository
        self.cep_lookup = cep_lookup

    def listar_enderecos(self, cep_input: str = "") -> list[dict[str, str]]:
        if cep_input:
            endereco = self.buscar_endereco_por_cep(cep_input)
            return [endereco] if endereco else []
        return [_formatar_endereco(row) for row in self.repository.listar_todos()]

    def buscar_endereco_por_cep(self, cep_input: str) -> dict[str, str] | None:
        cep = _normalizar_cep(cep_input)
        if cep is None:
            raise ValueError("Informe um CEP com 8 dígitos.")
        endereco = self.cep_lookup.buscar_por_cep(cep)
        return _formatar_endereco(endereco) if endereco else None

    def cadastrar_endereco(self, data: Any) -> dict[str, str]:
        if not isinstance(data, dict):
            raise ValueError("Envie os dados do endereço em JSON.")

        cep = _normalizar_cep(str(data.get("cep", "")))
        if cep is None:
            raise ValueError("Informe um CEP com 8 dígitos.")

        endereco = {
            "cep": cep,
            "logradouro": str(data.get("logradouro", "")).strip(),
            "bairro": str(data.get("bairro", "")).strip(),
            "cidade": str(data.get("cidade", "")).strip(),
            "uf": str(data.get("uf", "")).strip().upper(),
        }

        if any(not endereco[field] for field in ("logradouro", "bairro", "cidade", "uf")):
            raise ValueError("Preencha logradouro, bairro, cidade e UF.")
        if len(endereco["uf"]) != 2:
            raise ValueError("A UF deve conter 2 letras.")

        self.repository.salvar(endereco)
        return _formatar_endereco(endereco)


__all__ = ["CepDuplicadoError", "EnderecoService"]