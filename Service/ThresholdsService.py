from DTOs.ThresholdsRequestDTO import ThresholdsRequestDTO
from DTOs.ThresholdsResponseDTO import ThresholdsResponseDTO
from Repository.ThresholdsRepository import (
    selecionarTodosThresholds,
    buscarThresholdsPorId,
    selecionarPorChave,
    inserirThresholds,
    alterarThresholds,
    deletarThresholds,
    existePeloId,
)
from Repository.LocalidadesRepository import existePeloId as existeLocalidade
from Exception.exception import (
    ElementoNaoEncontradoException,
    ElementoCadastrado,
)


def selecionarTodos() -> list[ThresholdsResponseDTO]:

    dtoList = [ThresholdsResponseDTO.EntityToDTO(threshold) for threshold
               in selecionarTodosThresholds()]

    return dtoList

def selecionarPeloId(id: int) -> ThresholdsResponseDTO:

    obj = buscarThresholdsPorId(id)

    if obj is None:
        raise ElementoNaoEncontradoException(f"Threshold com o id: {id} não foi encontrada")

    return ThresholdsResponseDTO.EntityToDTO(obj)

def inserir(Threshold: ThresholdsRequestDTO) -> ThresholdsResponseDTO:

    if not existeLocalidade(Threshold.FKLocalidade):
        raise ElementoNaoEncontradoException(
            f"Localidade com o id: {Threshold.FKLocalidade} não foi encontrada!")

    obj = selecionarPorChave(
        Threshold.FKLocalidade,
        Threshold.Variavel,
        Threshold.TipoLimiar,
        Threshold.EstacaoDoAno,
    )

    if obj is not None:
        raise ElementoCadastrado(
            "Já existe um threshold para essa localidade, variável, tipo de limiar e estação do ano!")

    return ThresholdsResponseDTO.EntityToDTO(
        inserirThresholds(Threshold.dtoToEntity()))

def alterar(Threshold: ThresholdsRequestDTO) -> ThresholdsResponseDTO:

    if Threshold.IDThreshold is None:
        raise ElementoNaoEncontradoException("O id do threshold deve ser informado!")

    if not existePeloId(Threshold.IDThreshold):
        raise ElementoNaoEncontradoException(
            f"Threshold com o id: {Threshold.IDThreshold} não foi encontrada!")

    if not existeLocalidade(Threshold.FKLocalidade):
        raise ElementoNaoEncontradoException(
            f"Localidade com o id: {Threshold.FKLocalidade} não foi encontrada!")

    obj = selecionarPorChave(
        Threshold.FKLocalidade,
        Threshold.Variavel,
        Threshold.TipoLimiar,
        Threshold.EstacaoDoAno,
    )

    if obj is not None and obj.IDThreshold != Threshold.IDThreshold:
        raise ElementoCadastrado(
            "Já existe um threshold para essa localidade, variável, tipo de limiar e estação do ano!")

    return ThresholdsResponseDTO.EntityToDTO(
        alterarThresholds(Threshold.dtoToEntity()))

def excluir(id: int):

    if not existePeloId(id):
        raise ElementoNaoEncontradoException(f"Threshold com o id: {id} não foi encontrada!")

    deletarThresholds(id)
