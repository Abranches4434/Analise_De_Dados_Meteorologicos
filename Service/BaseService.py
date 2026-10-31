from abc import ABC, abstractmethod


class BaseService(ABC):
    """Contrato comum dos serviços de domínio."""

    def __init__(self, repositorio):
        self._repositorio = repositorio

    @property
    def repositorio(self):
        return self._repositorio

    @abstractmethod
    def selecionar_todos(self, incluir_inativos: bool = False):
        raise NotImplementedError

    @abstractmethod
    def selecionar_por_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def inserir(self, dto):
        raise NotImplementedError

    @abstractmethod
    def alterar(self, dto):
        raise NotImplementedError

    @abstractmethod
    def excluir(self, id: int):
        raise NotImplementedError
