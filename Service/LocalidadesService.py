from DTOs.LocalidadesResponseDTO import LocalidadesResponseDTO
from DTOs.LocalidadesRequestDTO import LocalidadesRequestDTO
from Repository.LocalidadesRepository import (
    selecionarTodasLocalidades,
    buscarLocalidadePorId,
    selecionarPorLatitudeELongitude,
    inserirLocalidade,
    alterarLocalidade,
    deletarLocalidade,
    existePeloId,
    existeDependencia,
)
from Exception.exception import (
    ElementoNaoEncontradoException,
    ElementoCadastrado,
    ElementoComDependenciasException,
)


def selecionarTodos() -> list[LocalidadesResponseDTO]:
    
    dtoList = [LocalidadesResponseDTO.EntityToDTO(localidade) for localidade 
                                                    in selecionarTodasLocalidades()]
    
    return dtoList

def selecionarPeloId(id: int) -> LocalidadesResponseDTO:
    
    obj = buscarLocalidadePorId(id)
    
    if obj is None:
        raise ElementoNaoEncontradoException(f"Localidade com o id: {id} não foi encontrada")

    return LocalidadesResponseDTO.EntityToDTO(obj)

def inserir(Localidade: LocalidadesRequestDTO) -> LocalidadesResponseDTO:

    obj = selecionarPorLatitudeELongitude(Localidade.Latitude, Localidade.Longitude)

    if obj is not None:
        raise ElementoCadastrado("Localidade já cadastrada no sistema!")

    return LocalidadesResponseDTO.EntityToDTO(inserirLocalidade(Localidade.dtoToEntity()))

def alterar(Localidade: LocalidadesRequestDTO) -> LocalidadesResponseDTO:

    if Localidade.IDLocalidade is None:
        raise ElementoNaoEncontradoException("O id da localidade deve ser informado!")

    if not existePeloId(Localidade.IDLocalidade):
        raise ElementoNaoEncontradoException(f"Localidade com o id: {Localidade.IDLocalidade} não foi encontrada!")

    return LocalidadesResponseDTO.EntityToDTO(alterarLocalidade(Localidade.dtoToEntity()))

def excluir(id: int):

    if not existePeloId(id):
        raise ElementoNaoEncontradoException(f"Localidade com o id: {id} não foi encontrada!")

    if existeDependencia(id):
        raise ElementoComDependenciasException(
            f"Localidade com o id: {id} possui registros ou thresholds vinculados e não pode ser excluída!")

    deletarLocalidade(id)
