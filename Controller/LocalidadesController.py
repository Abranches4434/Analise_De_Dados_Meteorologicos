from Controller.BaseController import BaseController
from DTOs.LocalidadesRequestDTO import LocalidadesRequestDTO
from DTOs.LocalidadesResponseDTO import LocalidadesResponseDTO
from Service.LocalidadesService import LocalidadesService


class LocalidadesController(BaseController):

    def __init__(self, servico: LocalidadesService | None = None):
        super().__init__(servico or LocalidadesService())

    def selecionar_todos(
        self,
        incluir_inativos: bool = False,
    ) -> list[LocalidadesResponseDTO]:
        return self.servico.selecionar_todos(incluir_inativos)

    def selecionar_por_id(self, id: int) -> LocalidadesResponseDTO:
        return self.servico.selecionar_por_id(id)

    def inserir(self, dados) -> LocalidadesResponseDTO:
        dto = self.converter_para_dto(dados, LocalidadesRequestDTO)
        return self.servico.inserir(dto)

    def alterar(self, dados, id: int) -> LocalidadesResponseDTO:
        dados_com_id = dict(dados or {})
        dados_com_id["IDLocalidade"] = id
        dto = self.converter_para_dto(
            dados_com_id,
            LocalidadesRequestDTO,
        )
        return self.servico.alterar(dto)

    def excluir(self, id: int):
        self.servico.excluir(id)
