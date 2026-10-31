from abc import ABC


class BaseController(ABC):
    """Controlador base com acesso encapsulado ao serviço."""

    def __init__(self, servico):
        self._servico = servico

    @property
    def servico(self):
        return self._servico

    @staticmethod
    def converter_para_dto(dados, classe_dto):
        if isinstance(dados, classe_dto):
            return dados

        return classe_dto(**(dados or {}))
