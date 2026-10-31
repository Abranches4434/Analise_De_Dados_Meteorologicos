from DTOs.LocalidadesRequestDTO import (
    LocalidadesRequestDTO,
    normalizarCoordenada,
)
from DTOs.LocalidadesResponseDTO import LocalidadesResponseDTO
from Exception.exception import (
    ElementoCadastrado,
    ElementoNaoEncontradoException,
)
from Repository.LocalidadesRepository import LocalidadesRepository
from Service.BaseService import BaseService


class LocalidadesService(BaseService):

    def __init__(self, repositorio: LocalidadesRepository | None = None):
        super().__init__(repositorio or LocalidadesRepository())

    def selecionar_todos(
        self,
        incluir_inativos: bool = False,
    ) -> list[LocalidadesResponseDTO]:
        return [
            LocalidadesResponseDTO.EntityToDTO(localidade)
            for localidade in self.repositorio.selecionar_todos(
                incluir_inativos
            )
        ]

    def selecionar_por_id(self, id: int) -> LocalidadesResponseDTO:
        localidade = self.repositorio.buscar_por_id(id)

        if localidade is None:
            raise ElementoNaoEncontradoException(
                f"Localidade com o id: {id} não foi encontrada"
            )

        return LocalidadesResponseDTO.EntityToDTO(localidade)

    def inserir(self, localidade: LocalidadesRequestDTO) -> LocalidadesResponseDTO:
        latitude = normalizarCoordenada(localidade.Latitude)
        longitude = normalizarCoordenada(localidade.Longitude)

        existente = self.repositorio.selecionar_por_coordenadas(
            latitude,
            longitude,
        )

        if existente is not None:
            raise ElementoCadastrado("Localidade já cadastrada no sistema!")

        return LocalidadesResponseDTO.EntityToDTO(
            self.repositorio.inserir(localidade.dtoToEntity())
        )

    def alterar(self, localidade: LocalidadesRequestDTO) -> LocalidadesResponseDTO:
        if localidade.IDLocalidade is None:
            raise ElementoNaoEncontradoException(
                "O id da localidade deve ser informado!"
            )

        if not self.repositorio.existe_por_id(localidade.IDLocalidade):
            raise ElementoNaoEncontradoException(
                f"Localidade com o id: {localidade.IDLocalidade} não foi encontrada!"
            )

        latitude = normalizarCoordenada(localidade.Latitude)
        longitude = normalizarCoordenada(localidade.Longitude)

        existente = self.repositorio.selecionar_por_coordenadas(
            latitude,
            longitude,
        )

        if (
            existente is not None
            and existente.IDLocalidade != localidade.IDLocalidade
        ):
            raise ElementoCadastrado(
                "Já existe outra localidade cadastrada com essa latitude e longitude!"
            )

        return LocalidadesResponseDTO.EntityToDTO(
            self.repositorio.alterar(localidade.dtoToEntity())
        )

    def excluir(self, id: int):
        if not self.repositorio.existe_por_id(id):
            raise ElementoNaoEncontradoException(
                f"Localidade com o id: {id} não foi encontrada!"
            )

        self.repositorio.inativar(id)
