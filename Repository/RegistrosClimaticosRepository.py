from datetime import date, time

from Entity.RegistrosClimaticos import RegistrosClimaticos
from Entity import db


def selecionarTodosRegistrosClimaticos(incluirInativos: bool = False) -> list[RegistrosClimaticos]:
    consulta = db.select(RegistrosClimaticos)

    if not incluirInativos:
        consulta = consulta.where(RegistrosClimaticos.Ativo.is_(True))

    return db.session.execute(consulta).scalars().all()

def buscarRegistrosClimaticosPorId(id):
    return db.session.get(RegistrosClimaticos, id)

def selecionarPorDataHoraELocalidade(Data: date, Hora: time, FKLocalidade: int) -> RegistrosClimaticos:
    return db.session.execute(
        db.select(RegistrosClimaticos).where(
            RegistrosClimaticos.Data == Data,
            RegistrosClimaticos.Hora == Hora,
            RegistrosClimaticos.FKLocalidade == FKLocalidade
        )
    ).scalars().first()

def inserirRegistrosClimaticos(Registro : RegistrosClimaticos) -> RegistrosClimaticos:
    db.session.add(Registro)
    db.session.commit()
    db.session.refresh(Registro)
    return Registro

def alterarRegistrosClimaticos(Registro : RegistrosClimaticos) -> RegistrosClimaticos:
    reg = db.session.get(RegistrosClimaticos, Registro.IDRegistrosClimaticos)

    if reg is not None:
        reg.Ativo = Registro.Ativo
        reg.Data = Registro.Data
        reg.FKLocalidade = Registro.FKLocalidade
        reg.Hora = Registro.Hora
        reg.Precipitacao = Registro.Precipitacao
        reg.PressaoAtmosferica = Registro.PressaoAtmosferica
        reg.TempMax = Registro.TempMax
        reg.TempMin = Registro.TempMin
        reg.UmidadeRelativa = Registro.UmidadeRelativa
        reg.VelocidadeVento = Registro.VelocidadeVento

        db.session.commit()

    return reg

def deletarRegistrosClimaticos(id):
    reg = db.session.get(RegistrosClimaticos, id)

    if reg is not None:
        reg.Ativo = False
        db.session.commit()


def existePeloId(id: int) -> bool:
    return bool(db.session.execute(
        db.select(db.exists().where(RegistrosClimaticos.IDRegistrosClimaticos == id))).scalar())
