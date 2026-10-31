from Controller.BaseController import BaseController
from DTOs.ThresholdsRequestDTO import ThresholdsRequestDTO
from DTOs.ThresholdsResponseDTO import ThresholdsResponseDTO
from Service.ThresholdsService import ThresholdsService


class ThresholdsController(BaseController):

    def __init__(self, servico: ThresholdsService | None = None):
        super().__init__(servico or ThresholdsService())

    def selecionar_todos(
        self,
        incluir_inativos: bool = False,
    ) -> list[ThresholdsResponseDTO]:
        return self.servico.selecionar_todos(incluir_inativos)

    def selecionar_por_id(self, id: int) -> ThresholdsResponseDTO:
        return self.servico.selecionar_por_id(id)

    def inserir(self, dados) -> ThresholdsResponseDTO:
        dto = self.converter_para_dto(dados, ThresholdsRequestDTO)
        return self.servico.inserir(dto)

    def alterar(self, dados, id: int) -> ThresholdsResponseDTO:
        dados_com_id = dict(dados or {})
        dados_com_id["IDThreshold"] = id
        dto = self.converter_para_dto(dados_com_id, ThresholdsRequestDTO)
        return self.servico.alterar(dto)

    def excluir(self, id: int):
        self.servico.excluir(id)
