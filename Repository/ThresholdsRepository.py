from Entity import db
from Entity.Thresholds import Thresholds
from Enum.Estacao import Estacao
from Enum.TipoLimiar import TipoLimiar
from Enum.Variavel import Variavel
from Repository.BaseRepository import BaseRepository


class ThresholdsRepository(BaseRepository):

    def __init__(self):
        super().__init__(Thresholds)

    def selecionar_por_chave(
        self,
        fk_localidade: int,
        variavel: Variavel,
        tipo_limiar: TipoLimiar,
        estacao_do_ano: Estacao,
    ) -> Thresholds | None:
        return db.session.execute(
            db.select(Thresholds).where(
                Thresholds.FKLocalidade == fk_localidade,
                Thresholds.Variavel == variavel,
                Thresholds.TipoLimiar == tipo_limiar,
                Thresholds.EstacaoDoAno == estacao_do_ano,
            )
        ).scalars().first()

    def alterar(self, threshold: Thresholds) -> Thresholds | None:
        threshold_atual = self.buscar_por_id(threshold.IDThreshold)

        if threshold_atual is not None:
            threshold_atual.FKLocalidade = threshold.FKLocalidade
            threshold_atual.Ativo = threshold.Ativo
            threshold_atual.EstacaoDoAno = threshold.EstacaoDoAno
            threshold_atual.TipoLimiar = threshold.TipoLimiar
            threshold_atual.Valor = threshold.Valor
            threshold_atual.Variavel = threshold.Variavel
            db.session.commit()

        return threshold_atual
