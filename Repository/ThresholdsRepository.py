from Entity.Thresholds import Thresholds
from Entity import db


def selecionarTodosThresholds():
    return db.session.execute(db.select(Thresholds)).scalars().all()

def buscarThresholdsPorId(id):
    return db.session.get(Thresholds, id)

def inserirThresholds(thresholds : Thresholds):
    db.session.add(thresholds)
    db.session.commit()
    db.session.refresh(thresholds)
    return thresholds

def alterarThresholds(thresholds : Thresholds):
    td = db.session.get(Thresholds, thresholds.IDThreshold)


    if td is not None: 
        td.FKLocalidade = thresholds.FKLocalidade
        td.Ativo = thresholds.Ativo
        td.EstacaoDoAno = thresholds.EstacaoDoAno
        td.TipoLimiar = thresholds.TipoLimiar
        td.Valor = thresholds.Valor
        td.Variavel = thresholds.Variavel

        db.commit()

def deletarThresholds(id):
    reg = db.session.get(Thresholds, id)

    if reg is not None:
        db.session.delete(reg)
        db.session.commit()