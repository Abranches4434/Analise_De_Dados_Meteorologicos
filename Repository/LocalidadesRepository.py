from decimal import Decimal

from Entity import db
from Entity.Localidades import Localidades
from Entity.RegistrosClimaticos import RegistrosClimaticos
from Entity.Thresholds import Thresholds
from Repository.BaseRepository import BaseRepository


class LocalidadesRepository(BaseRepository):

    def __init__(self):
        super().__init__(Localidades)

    def selecionar_por_coordenadas(
        self,
        latitude: Decimal,
        longitude: Decimal,
    ) -> Localidades | None:
        return db.session.execute(
            db.select(Localidades).where(
                Localidades.Latitude == latitude,
                Localidades.Longitude == longitude,
            )
        ).scalars().first()

    def alterar(self, localidade: Localidades) -> Localidades | None:
        localidade_atual = self.buscar_por_id(localidade.IDLocalidade)

        if localidade_atual is not None:
            localidade_atual.Nome = localidade.Nome
            localidade_atual.Cidade = localidade.Cidade
            localidade_atual.Estado = localidade.Estado
            localidade_atual.Latitude = localidade.Latitude
            localidade_atual.Longitude = localidade.Longitude
            localidade_atual.Ativo = localidade.Ativo
            db.session.commit()

        return localidade_atual

    def existe_dependencia(self, id: int) -> bool:
        possui_registro = db.session.execute(
            db.select(
                db.exists().where(RegistrosClimaticos.FKLocalidade == id)
            )
        ).scalar()
        possui_threshold = db.session.execute(
            db.select(
                db.exists().where(Thresholds.FKLocalidade == id)
            )
        ).scalar()

        return bool(possui_registro or possui_threshold)
