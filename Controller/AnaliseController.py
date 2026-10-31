from Controller.BaseController import BaseController
from Service.AnaliseService import AnaliseService


class AnaliseController(BaseController):

    def __init__(self):
        super().__init__(AnaliseService())

    def estatisticas(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
    ) -> dict:
        return self.servico.estatisticas(
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
        )

    def comparar(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_ids: list[int] | None = None,
    ) -> dict:
        return self.servico.comparar(
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_ids=localidade_ids or [],
        )

    def eventos_extremos(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
    ) -> dict:
        return self.servico.eventos_extremos(
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
        )

    def sazonalidade(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
        agrupamento: str = "mes",
    ) -> dict:
        return self.servico.sazonalidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
            agrupamento=agrupamento,
        )

    def exportar(
        self,
        tipo: str,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
        localidade_ids: list[int] | None = None,
        agrupamento: str = "mes",
    ) -> tuple[str, str]:
        return self.servico.exportar(
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
            localidade_ids=localidade_ids or [],
            agrupamento=agrupamento,
        )
