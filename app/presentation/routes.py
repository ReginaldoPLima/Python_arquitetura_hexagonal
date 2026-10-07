from flask import Blueprint, current_app, jsonify, render_template, request

from app.domain.errors import CepDuplicadoError, CepProviderError
from app.service.endereco_service import EnderecoService


presentation = Blueprint("presentation", __name__)


def _endereco_service() -> EnderecoService:
    return current_app.extensions["endereco_service"]


@presentation.get("/")
def index():
    return render_template("index.html")


@presentation.get("/api/enderecos")
def get_addresses():
    try:
        addresses = _endereco_service().listar_enderecos(request.args.get("cep", "").strip())
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400
    except CepProviderError as error:
        return jsonify({"erro": str(error)}), 502
    return jsonify({"enderecos": addresses})


@presentation.get("/api/enderecos/cep/<cep>")
def get_address_by_cep(cep: str):
    try:
        address = _endereco_service().buscar_endereco_por_cep(cep)
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400
    except CepProviderError as error:
        return jsonify({"erro": str(error)}), 502
    if address is None:
        return jsonify({"erro": "Endereço não encontrado para este CEP."}), 404
    return jsonify({"endereco": address})


@presentation.post("/api/enderecos")
def post_address():
    try:
        address = _endereco_service().cadastrar_endereco(request.get_json(silent=True))
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400
    except CepDuplicadoError:
        return jsonify({"erro": "Já existe um endereço cadastrado para este CEP."}), 409
    return jsonify({"endereco": address}), 201