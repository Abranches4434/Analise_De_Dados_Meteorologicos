from Entity.Thresholds import Thresholds
from Entity import db
from Enum.Variavel import Variavel
from Enum.TipoLimiar import TipoLimiar
from Enum.Estacao import Estacao


def selecionarTodosThresholds() -> list[Thresholds]:
    return db.session.execute(db.select(Thresholds)).scalars().all()

def buscarThresholdsPorId(id):
    return db.session.get(Thresholds, id)

def selecionarPorChave(FKLocalidade: int, Variavel: Variavel,
                       TipoLimiar: TipoLimiar, EstacaoDoAno: Estacao) -> Thresholds:
    return db.session.execute(
        db.select(Thresholds).where(
            Thresholds.FKLocalidade == FKLocalidade,
            Thresholds.Variavel == Variavel,
            Thresholds.TipoLimiar == TipoLimiar,
            Thresholds.EstacaoDoAno == EstacaoDoAno
        )
    ).scalars().first()

def inserirThresholds(thresholds : Thresholds) -> Thresholds:
    db.session.add(thresholds)
    db.session.commit()
    db.session.refresh(thresholds)
    return thresholds

def alterarThresholds(thresholds : Thresholds) -> Thresholds:
    td = db.session.get(Thresholds, thresholds.IDThreshold)

    if td is not None:
        td.FKLocalidade = thresholds.FKLocalidade
        td.Ativo = thresholds.Ativo
        td.EstacaoDoAno = thresholds.EstacaoDoAno
        td.TipoLimiar = thresholds.TipoLimiar
        td.Valor = thresholds.Valor
        td.Variavel = thresholds.Variavel

        db.session.commit()

    return td

def deletarThresholds(id):
    reg = db.session.get(Thresholds, id)

    if reg is not None:
        db.session.delete(reg)
        db.session.commit()


def existePeloId(id: int) -> bool:
    return bool(db.session.execute(
        db.select(db.exists().where(Thresholds.IDThreshold == id))).scalar())
