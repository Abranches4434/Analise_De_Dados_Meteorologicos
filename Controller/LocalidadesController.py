from flask import jsonify
from pydantic import ValidationError

from DTOs.LocalidadesRequestDTO import LocalidadesRequestDTO
from DTOs.LocalidadesResponseDTO import LocalidadesResponseDTO
from Exception.exception import (
    ElementoNaoEncontradoException,
    ElementoCadastrado,
    ElementoComDependenciasException,
)
from Service.LocalidadesService import (
    selecionarTodos,
    selecionarPeloId,
    inserir,
    alterar,
    excluir,
)


def _toDTO(dados) -> LocalidadesRequestDTO:
    if isinstance(dados, LocalidadesRequestDTO):
        return dados

    return LocalidadesRequestDTO(**dados)


def inserirLocalidade(Localidade) -> LocalidadesResponseDTO:

    try:
        dto = _toDTO(Localidade)
        return jsonify(inserir(dto).model_dump(mode="json")), 201
    except ValidationError as error:
        return jsonify({
            "erro": str(error)
        }), 400
    except ElementoCadastrado as error:
        return jsonify({
            "erro": str(error)
        }), 409
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500

def selecionarTodasLocalidades() -> list[LocalidadesResponseDTO]:

    try:
        dtos = selecionarTodos()
        return jsonify([dto.model_dump(mode="json") for dto in dtos]), 200
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500
    

def selecionarLocalidadePeloID(id : int) -> LocalidadesResponseDTO:

    try:
        return jsonify(selecionarPeloId(id).model_dump(mode="json")), 200
    except ElementoNaoEncontradoException as error:
        return jsonify({
            "erro": str(error)
        }), 404
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500
    

def alterarLocalidade(Localidade) -> LocalidadesResponseDTO:

    try:
        dto = _toDTO(Localidade)
        return jsonify(alterar(dto).model_dump(mode="json")), 200
    except ValidationError as error:
        return jsonify({
            "erro": str(error)
        }), 400
    except ElementoNaoEncontradoException as error:
        return jsonify({
            "erro": str(error)
        }), 404
    except ElementoCadastrado as error:
        return jsonify({
            "erro": str(error)
        }), 409
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500
    

def deletarLocalidadePeloId(id : int) -> LocalidadesResponseDTO:

    try:
        excluir(id)
        return "", 204
    except ElementoNaoEncontradoException as error:
        return jsonify({
            "erro": str(error)
        }), 404
    except ElementoComDependenciasException as error:
        return jsonify({
            "erro": str(error)
        }), 409
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500
