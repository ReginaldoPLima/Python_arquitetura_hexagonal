import re
from typing import Any

from app.repository import endereco_repository
from app.repository.endereco_repository import CepDuplicadoError


def _normalizar_cep(value: str) -> str | None:
    cep = re.sub(r"\D", "", value)
    return cep if len(cep) == 8 else None


def _formatar_endereco(row: Any) -> dict[str, str]:
    endereco = dict(row)
    endereco["cep"] = f"{endereco['cep'][:5]}-{endereco['cep'][5:]}"
    return endereco


def listar_enderecos(cep_input: str = "") -> list[dict[str, str]]:
    if cep_input:
        cep = _normalizar_cep(cep_input)
        if cep is None:
            raise ValueError("Informe um CEP com 8 dígitos.")
        endereco = endereco_repository.buscar_por_cep(cep)
        return [_formatar_endereco(endereco)] if endereco else []

    return [_formatar_endereco(row) for row in endereco_repository.listar_todos()]


def cadastrar_endereco(data: Any) -> dict[str, str]:
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

    endereco_repository.salvar(endereco)
    return _formatar_endereco(endereco)


__all__ = ["CepDuplicadoError", "cadastrar_endereco", "listar_enderecos"]