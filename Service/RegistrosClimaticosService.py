from DTOs.RegistrosClimaticosRequestDTO import RegistrosClimaticosRequestDTO
from DTOs.RegistrosClimaticosResponseDTO import RegistrosClimaticosResponseDTO
from Exception.exception import (
    ElementoCadastrado,
    ElementoNaoEncontradoException,
)
from Repository.LocalidadesRepository import LocalidadesRepository
from Repository.RegistrosClimaticosRepository import (
    RegistrosClimaticosRepository,
)
from Service.BaseService import BaseService


class RegistrosClimaticosService(BaseService):

    def __init__(
        self,
        repositorio: RegistrosClimaticosRepository | None = None,
        localidades_repositorio: LocalidadesRepository | None = None,
    ):
        super().__init__(repositorio or RegistrosClimaticosRepository())
        self._localidades_repositorio = (
            localidades_repositorio or LocalidadesRepository()
        )

    @property
    def localidades_repositorio(self) -> LocalidadesRepository:
        return self._localidades_repositorio

    def selecionar_todos(
        self,
        incluir_inativos: bool = False,
    ) -> list[RegistrosClimaticosResponseDTO]:
        return [
            RegistrosClimaticosResponseDTO.EntityToDTO(registro)
            for registro in self.repositorio.selecionar_todos(
                incluir_inativos
            )
        ]

    def selecionar_por_id(self, id: int) -> RegistrosClimaticosResponseDTO:
        registro = self.repositorio.buscar_por_id(id)

        if registro is None:
            raise ElementoNaoEncontradoException(
                f"Registro com o id: {id} não foi encontrado"
            )

        return RegistrosClimaticosResponseDTO.EntityToDTO(registro)

    def inserir(
        self,
        registro: RegistrosClimaticosRequestDTO,
    ) -> RegistrosClimaticosResponseDTO:
        if not self.localidades_repositorio.existe_ativo_por_id(
            registro.FKLocalidade
        ):
            raise ElementoNaoEncontradoException(
                f"Localidade ativa com o id: {registro.FKLocalidade} não foi encontrada!"
            )

        existente = self.repositorio.selecionar_por_data_hora_localidade(
            registro.Data,
            registro.Hora,
            registro.FKLocalidade,
        )

        if existente is not None:
            raise ElementoCadastrado(
                "Já existe um registro para essa data, hora e localidade!"
            )

        return RegistrosClimaticosResponseDTO.EntityToDTO(
            self.repositorio.inserir(registro.dtoToEntity())
        )

    def alterar(
        self,
        registro: RegistrosClimaticosRequestDTO,
    ) -> RegistrosClimaticosResponseDTO:
        if registro.IDRegistrosClimaticos is None:
            raise ElementoNaoEncontradoException(
                "O id do registro deve ser informado!"
            )

        if not self.repositorio.existe_por_id(
            registro.IDRegistrosClimaticos
        ):
            raise ElementoNaoEncontradoException(
                f"Registro com o id: {registro.IDRegistrosClimaticos} não foi encontrado!"
            )

        if not self.localidades_repositorio.existe_ativo_por_id(
            registro.FKLocalidade
        ):
            raise ElementoNaoEncontradoException(
                f"Localidade ativa com o id: {registro.FKLocalidade} não foi encontrada!"
            )

        existente = self.repositorio.selecionar_por_data_hora_localidade(
            registro.Data,
            registro.Hora,
            registro.FKLocalidade,
        )

        if (
            existente is not None
            and existente.IDRegistrosClimaticos
            != registro.IDRegistrosClimaticos
        ):
            raise ElementoCadastrado(
                "Já existe um registro para essa data, hora e localidade!"
            )

        return RegistrosClimaticosResponseDTO.EntityToDTO(
            self.repositorio.alterar(registro.dtoToEntity())
        )

    def excluir(self, id: int):
        if not self.repositorio.existe_por_id(id):
            raise ElementoNaoEncontradoException(
                f"Registro com o id: {id} não foi encontrado!"
            )

        self.repositorio.inativar(id)
