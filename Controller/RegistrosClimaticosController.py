from flask import jsonify
from pydantic import ValidationError

from DTOs.RegistrosClimaticosRequestDTO import RegistrosClimaticosRequestDTO
from DTOs.RegistrosClimaticosResponseDTO import RegistrosClimaticosResponseDTO
from Exception.exception import (
    ElementoNaoEncontradoException,
    ElementoCadastrado,
)
from Service.RegistrosClimaticosService import (
    selecionarTodos,
    selecionarPeloId,
    inserir,
    alterar,
    excluir,
)


def _toDTO(dados) -> RegistrosClimaticosRequestDTO:
    if isinstance(dados, RegistrosClimaticosRequestDTO):
        return dados

    return RegistrosClimaticosRequestDTO(**dados)


def inserirRegistro(Registro) -> RegistrosClimaticosResponseDTO:

    try:
        dto = _toDTO(Registro)
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

def selecionarTodosRegistros() -> list[RegistrosClimaticosResponseDTO]:

    try:
        dtos = selecionarTodos()
        return jsonify([dto.model_dump(mode="json") for dto in dtos]), 200
    except Exception as error:
        return jsonify({
            "erro": str(error)
        }), 500

def selecionarRegistroPeloID(id : int) -> RegistrosClimaticosResponseDTO:

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

def alterarRegistro(Registro) -> RegistrosClimaticosResponseDTO:

    try:
        dto = _toDTO(Registro)
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

def deletarRegistroPeloId(id : int) -> RegistrosClimaticosResponseDTO:

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
