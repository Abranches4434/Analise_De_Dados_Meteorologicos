from DTOs.ThresholdsRequestDTO import ThresholdsRequestDTO
from DTOs.ThresholdsResponseDTO import ThresholdsResponseDTO
from Exception.exception import (
    ElementoCadastrado,
    ElementoNaoEncontradoException,
)
from Repository.LocalidadesRepository import LocalidadesRepository
from Repository.ThresholdsRepository import ThresholdsRepository
from Service.BaseService import BaseService


class ThresholdsService(BaseService):

    def __init__(
        self,
        repositorio: ThresholdsRepository | None = None,
        localidades_repositorio: LocalidadesRepository | None = None,
    ):
        super().__init__(repositorio or ThresholdsRepository())
        self._localidades_repositorio = (
            localidades_repositorio or LocalidadesRepository()
        )

    @property
    def localidades_repositorio(self) -> LocalidadesRepository:
        return self._localidades_repositorio

    def selecionar_todos(
        self,
        incluir_inativos: bool = False,
    ) -> list[ThresholdsResponseDTO]:
        return [
            ThresholdsResponseDTO.EntityToDTO(threshold)
            for threshold in self.repositorio.selecionar_todos(
                incluir_inativos
            )
        ]

    def selecionar_por_id(self, id: int) -> ThresholdsResponseDTO:
        threshold = self.repositorio.buscar_por_id(id)

        if threshold is None:
            raise ElementoNaoEncontradoException(
                f"Threshold com o id: {id} não foi encontrada"
            )

        return ThresholdsResponseDTO.EntityToDTO(threshold)

    def inserir(
        self,
        threshold: ThresholdsRequestDTO,
    ) -> ThresholdsResponseDTO:
        if not self.localidades_repositorio.existe_ativo_por_id(
            threshold.FKLocalidade
        ):
            raise ElementoNaoEncontradoException(
                f"Localidade ativa com o id: {threshold.FKLocalidade} não foi encontrada!"
            )

        existente = self.repositorio.selecionar_por_chave(
            threshold.FKLocalidade,
            threshold.Variavel,
            threshold.TipoLimiar,
            threshold.EstacaoDoAno,
        )

        if existente is not None:
            raise ElementoCadastrado(
                "Já existe um threshold para essa localidade, variável, tipo de limiar e estação do ano!"
            )

        return ThresholdsResponseDTO.EntityToDTO(
            self.repositorio.inserir(threshold.dtoToEntity())
        )

    def alterar(
        self,
        threshold: ThresholdsRequestDTO,
    ) -> ThresholdsResponseDTO:
        if threshold.IDThreshold is None:
            raise ElementoNaoEncontradoException(
                "O id do threshold deve ser informado!"
            )

        if not self.repositorio.existe_por_id(threshold.IDThreshold):
            raise ElementoNaoEncontradoException(
                f"Threshold com o id: {threshold.IDThreshold} não foi encontrada!"
            )

        if not self.localidades_repositorio.existe_ativo_por_id(
            threshold.FKLocalidade
        ):
            raise ElementoNaoEncontradoException(
                f"Localidade ativa com o id: {threshold.FKLocalidade} não foi encontrada!"
            )

        existente = self.repositorio.selecionar_por_chave(
            threshold.FKLocalidade,
            threshold.Variavel,
            threshold.TipoLimiar,
            threshold.EstacaoDoAno,
        )

        if (
            existente is not None
            and existente.IDThreshold != threshold.IDThreshold
        ):
            raise ElementoCadastrado(
                "Já existe um threshold para essa localidade, variável, tipo de limiar e estação do ano!"
            )

        return ThresholdsResponseDTO.EntityToDTO(
            self.repositorio.alterar(threshold.dtoToEntity())
        )

    def excluir(self, id: int):
        if not self.repositorio.existe_por_id(id):
            raise ElementoNaoEncontradoException(
                f"Threshold com o id: {id} não foi encontrada!"
            )

        self.repositorio.inativar(id)
