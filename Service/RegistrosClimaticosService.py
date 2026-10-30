from DTOs.RegistrosClimaticosRequestDTO import RegistrosClimaticosRequestDTO
from DTOs.RegistrosClimaticosResponseDTO import RegistrosClimaticosResponseDTO
from Repository.RegistrosClimaticosRepository import (
    selecionarTodosRegistrosClimaticos,
    buscarRegistrosClimaticosPorId,
    selecionarPorDataHoraELocalidade,
    inserirRegistrosClimaticos,
    alterarRegistrosClimaticos,
    deletarRegistrosClimaticos,
    existePeloId,
)
from Repository.LocalidadesRepository import existePeloId as existeLocalidade
from Exception.exception import (
    ElementoNaoEncontradoException,
    ElementoCadastrado,
)


def selecionarTodos() -> list[RegistrosClimaticosResponseDTO]:

    dtoList = [RegistrosClimaticosResponseDTO.EntityToDTO(registro) for registro
               in selecionarTodosRegistrosClimaticos()]

    return dtoList

def selecionarPeloId(id: int) -> RegistrosClimaticosResponseDTO:

    obj = buscarRegistrosClimaticosPorId(id)

    if obj is None:
        raise ElementoNaoEncontradoException(f"Registro com o id: {id} não foi encontrado")

    return RegistrosClimaticosResponseDTO.EntityToDTO(obj)

def inserir(Registro: RegistrosClimaticosRequestDTO) -> RegistrosClimaticosResponseDTO:

    if not existeLocalidade(Registro.FKLocalidade):
        raise ElementoNaoEncontradoException(
            f"Localidade com o id: {Registro.FKLocalidade} não foi encontrada!")

    obj = selecionarPorDataHoraELocalidade(Registro.Data, Registro.Hora, Registro.FKLocalidade)

    if obj is not None:
        raise ElementoCadastrado(
            "Já existe um registro para essa data, hora e localidade!")

    return RegistrosClimaticosResponseDTO.EntityToDTO(
        inserirRegistrosClimaticos(Registro.dtoToEntity()))

def alterar(Registro: RegistrosClimaticosRequestDTO) -> RegistrosClimaticosResponseDTO:

    if Registro.IDRegistrosClimaticos is None:
        raise ElementoNaoEncontradoException("O id do registro deve ser informado!")

    if not existePeloId(Registro.IDRegistrosClimaticos):
        raise ElementoNaoEncontradoException(
            f"Registro com o id: {Registro.IDRegistrosClimaticos} não foi encontrado!")

    if not existeLocalidade(Registro.FKLocalidade):
        raise ElementoNaoEncontradoException(
            f"Localidade com o id: {Registro.FKLocalidade} não foi encontrada!")

    obj = selecionarPorDataHoraELocalidade(Registro.Data, Registro.Hora, Registro.FKLocalidade)

    if obj is not None and obj.IDRegistrosClimaticos != Registro.IDRegistrosClimaticos:
        raise ElementoCadastrado(
            "Já existe um registro para essa data, hora e localidade!")

    return RegistrosClimaticosResponseDTO.EntityToDTO(
        alterarRegistrosClimaticos(Registro.dtoToEntity()))

def excluir(id: int):

    if not existePeloId(id):
        raise ElementoNaoEncontradoException(f"Registro com o id: {id} não foi encontrado!")

    deletarRegistrosClimaticos(id)
