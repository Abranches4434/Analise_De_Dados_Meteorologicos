from datetime import date, time

from Entity import db
from Entity.RegistrosClimaticos import RegistrosClimaticos
from Repository.BaseRepository import BaseRepository


class RegistrosClimaticosRepository(BaseRepository):

    def __init__(self):
        super().__init__(RegistrosClimaticos)

    def selecionar_por_data_hora_localidade(
        self,
        data: date,
        hora: time,
        fk_localidade: int,
    ) -> RegistrosClimaticos | None:
        return db.session.execute(
            db.select(RegistrosClimaticos).where(
                RegistrosClimaticos.Data == data,
                RegistrosClimaticos.Hora == hora,
                RegistrosClimaticos.FKLocalidade == fk_localidade,
            )
        ).scalars().first()

    def alterar(self, registro: RegistrosClimaticos) -> RegistrosClimaticos | None:
        registro_atual = self.buscar_por_id(
            registro.IDRegistrosClimaticos
        )

        if registro_atual is not None:
            registro_atual.Ativo = registro.Ativo
            registro_atual.Data = registro.Data
            registro_atual.FKLocalidade = registro.FKLocalidade
            registro_atual.Hora = registro.Hora
            registro_atual.Precipitacao = registro.Precipitacao
            registro_atual.PressaoAtmosferica = registro.PressaoAtmosferica
            registro_atual.TempMax = registro.TempMax
            registro_atual.TempMin = registro.TempMin
            registro_atual.TempMedia = registro.TempMedia
            registro_atual.UmidadeRelativa = registro.UmidadeRelativa
            registro_atual.VelocidadeVento = registro.VelocidadeVento
            db.session.commit()

        return registro_atual
