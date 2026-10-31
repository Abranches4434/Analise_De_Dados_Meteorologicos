from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from Exception.exception import (
    ElementoCadastrado,
    ElementoComDependenciasException,
    ElementoNaoEncontradoException,
)


class BaseResource(Resource):
    """Recurso REST base com serialização e tratamento de erros padronizados."""

    def _incluir_inativos(self) -> bool:
        valor = str(request.args.get("incluir_inativos", "")).lower()
        return valor in {"1", "true", "sim", "yes"}

    def _executar(self, acao, status: int = 200):
        try:
            resultado = acao()

            if resultado is None:
                return "", 204

            if isinstance(resultado, list):
                return [
                    item.model_dump(mode="json") for item in resultado
                ], status

            if hasattr(resultado, "model_dump"):
                return resultado.model_dump(mode="json"), status

            return resultado, status
        except ValidationError as erro:
            return {"erro": str(erro)}, 400
        except ElementoNaoEncontradoException as erro:
            return {"erro": str(erro)}, 404
        except ElementoCadastrado as erro:
            return {"erro": str(erro)}, 409
        except ElementoComDependenciasException as erro:
            return {"erro": str(erro)}, 409
        except Exception as erro:
            return {"erro": str(erro)}, 500
