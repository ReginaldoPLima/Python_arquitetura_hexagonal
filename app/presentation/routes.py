from flask import Blueprint, jsonify, render_template, request

from app.service.endereco_service import (
    CepDuplicadoError,
    cadastrar_endereco,
    listar_enderecos,
)


presentation = Blueprint("presentation", __name__)


@presentation.get("/")
def index():
    return render_template("index.html")


@presentation.get("/api/enderecos")
def get_addresses():
    try:
        addresses = listar_enderecos(request.args.get("cep", "").strip())
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400
    return jsonify({"enderecos": addresses})


@presentation.post("/api/enderecos")
def post_address():
    try:
        address = cadastrar_endereco(request.get_json(silent=True))
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400
    except CepDuplicadoError:
        return jsonify({"erro": "Já existe um endereço cadastrado para este CEP."}), 409
    return jsonify({"endereco": address}), 201