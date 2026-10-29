from Entity.Localidades import Localidades
from Entity.RegistrosClimaticos import RegistrosClimaticos
from Entity.Thresholds import Thresholds
from Entity import db


def selecionarTodasLocalidades() -> list[Localidades]:
    return db.session.execute(db.select(Localidades)).scalars().all()

def buscarLocalidadePorId(id):
    return db.session.get(Localidades, id)

def selecionarPorLatitudeELongitude(Latitude: float, Longitude: float) -> Localidades:
    
    return db.session.execute(db.select(Localidades).where(Localidades.Latitude == Latitude, 
                                                               Localidades.Longitude == Longitude)).scalars().first()

def inserirLocalidade(Localidade : Localidades):
    db.session.add(Localidade)
    db.session.commit()
    db.session.refresh(Localidade)
    return Localidade

def alterarLocalidade(Localidade : Localidades) -> Localidades:
    loc = db.session.get(Localidades, Localidade.IDLocalidade)


    if loc is not None: 
        loc.Nome = Localidade.Nome
        loc.Cidade = Localidade.Cidade
        loc.Estado = Localidade.Estado
        loc.Latitude = Localidade.Latitude
        loc.Longitude = Localidade.Longitude
        loc.Ativo = Localidade.Ativo

        db.session.commit()

    return loc

def deletarLocalidade(id):
    loc = db.session.get(Localidades, id)

    if loc is not None:
        db.session.delete(loc)
        db.session.commit()


def existePeloId(id: int) -> bool:
    return bool(db.session.execute(db.select(db.exists().where(Localidades.IDLocalidade == id))).scalar())

def existeDependencia(id: int) -> bool:
    possuiRegistro = db.session.execute(
        db.select(db.exists().where(RegistrosClimaticos.FKLocalidade == id))).scalar()
    possuiThreshold = db.session.execute(
        db.select(db.exists().where(Thresholds.FKLocalidade == id))).scalar()

    return bool(possuiRegistro or possuiThreshold)
