from flask import jsonify
from pydantic import ValidationError

from DTOs.ThresholdsRequestDTO import ThresholdsRequestDTO
from DTOs.ThresholdsResponseDTO import ThresholdsResponseDTO
from Exception.exception import (
    ElementoNaoEncontradoException,
    ElementoCadastrado,
)
from Service.ThresholdsService import (
    selecionarTodos,
    selecionarPeloId,
    inserir,
    alterar,
    excluir,
)


def _toDTO(dados) -> ThresholdsRequestDTO:
    if isinstance(dados, ThresholdsRequestDTO):
        return dados

    return ThresholdsRequestDTO(**dados)


def inserirThreshold(Threshold) -> ThresholdsResponseDTO:

    try:
        dto = _toDTO(Threshold)
        return jsonify(inserir(dto).model_dump(mode="json")), 201
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

def selecionarTodasThresholds() -> list[ThresholdsResponseDTO]:

    try:
        dtos = selecionarTodos()
        return jsonify([dto.model_dump(mode="json") for dto in dtos]), 200
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500

def selecionarThresholdPeloID(id : int) -> ThresholdsResponseDTO:

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

def alterarThreshold(Threshold) -> ThresholdsResponseDTO:

    try:
        dto = _toDTO(Threshold)
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

def deletarThresholdPeloId(id : int) -> ThresholdsResponseDTO:

    try:
        excluir(id)
        return "", 204
    except ElementoNaoEncontradoException as error:
        return jsonify({
            "erro": str(error)
        }), 404
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500
