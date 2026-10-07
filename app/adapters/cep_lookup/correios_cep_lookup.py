import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.domain.errors import CepProviderError
from app.domain.ports.cep_lookup import CepLookupPort


class CorreiosCepLookup(CepLookupPort):
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url.rstrip("/")
        self.api_token = api_token

    def buscar_por_cep(self, cep: str) -> dict[str, str] | None:
        try:
            request = Request(
                f"{self.api_url}/{cep}",
                headers={"Authorization": f"Bearer {self.api_token}"},
            )
            with urlopen(request, timeout=10) as response:
                data = json.load(response)
        except HTTPError as error:
            if error.code == 404:
                return None
            raise CepProviderError("Não foi possível consultar a API dos Correios.") from error
        except (URLError, TimeoutError, ValueError) as error:
            raise CepProviderError("Não foi possível consultar a API dos Correios.") from error

        if not isinstance(data, dict):
            raise CepProviderError("A API dos Correios retornou uma resposta inválida.")

        address = {
            "cep": str(data.get("cep", cep)).replace("-", ""),
            "logradouro": str(data.get("logradouro", "")).strip(),
            "bairro": str(data.get("bairro", "")).strip(),
            "cidade": str(data.get("cidade", data.get("localidade", ""))).strip(),
            "uf": str(data.get("uf", "")).strip().upper(),
        }
        if not all(address[field] for field in ("logradouro", "bairro", "cidade", "uf")):
            raise CepProviderError("A API dos Correios retornou dados incompletos para o CEP.")
        return address