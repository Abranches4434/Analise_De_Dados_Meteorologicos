from Controller.BaseController import BaseController
from DTOs.RegistrosClimaticosRequestDTO import RegistrosClimaticosRequestDTO
from DTOs.RegistrosClimaticosResponseDTO import RegistrosClimaticosResponseDTO
from Service.RegistrosClimaticosService import RegistrosClimaticosService


class RegistrosClimaticosController(BaseController):

    def __init__(
        self,
        servico: RegistrosClimaticosService | None = None,
    ):
        super().__init__(servico or RegistrosClimaticosService())

    def selecionar_todos(
        self,
        incluir_inativos: bool = False,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
    ) -> list[RegistrosClimaticosResponseDTO]:
        return self.servico.selecionar_todos(
            incluir_inativos=incluir_inativos,
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
        )

    def selecionar_por_id(self, id: int) -> RegistrosClimaticosResponseDTO:
        return self.servico.selecionar_por_id(id)

    def inserir(self, dados) -> RegistrosClimaticosResponseDTO:
        dto = self.converter_para_dto(
            dados,
            RegistrosClimaticosRequestDTO,
        )
        return self.servico.inserir(dto)

    def alterar(self, dados, id: int) -> RegistrosClimaticosResponseDTO:
        dados_com_id = dict(dados or {})
        dados_com_id["IDRegistrosClimaticos"] = id
        dto = self.converter_para_dto(
            dados_com_id,
            RegistrosClimaticosRequestDTO,
        )
        return self.servico.alterar(dto)

    def excluir(self, id: int):
        self.servico.excluir(id)
