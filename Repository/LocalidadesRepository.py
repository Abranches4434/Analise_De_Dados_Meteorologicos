from Entity.Localidades import Localidades
from Entity import db


def selecionarTodasLocalidades():
    return db.session.execute(db.select(Localidades)).scalars().all()

def buscarLocalidadePorId(id):
    return db.session.get(Localidades, id)

def inserirLocalidade(Localidade : Localidades):
    db.session.add(Localidade)
    db.session.commit()
    db.session.refresh(Localidade)
    return Localidade

def alterarLocalidade(Localidade : Localidades):
    loc = db.session.get(Localidades, Localidade.IDLocalidade)


    if loc is not None: 
        loc.Nome = Localidade.Nome
        loc.Cidade = Localidade.Cidade
        loc.Estado = Localidade.Estado
        loc.Latitude = Localidade.Latitude
        loc.Longitude = Localidade.Longitude
        loc.Ativo = Localidade.Ativo

        db.commit()

def deletarLocalidade(id):
    loc = db.session.get(Localidades, id)

    if loc is not None:
        db.session.delete(loc)
        db.session.commit()