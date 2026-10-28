from Entity.RegistrosClimaticos import RegistrosClimaticos
from Entity import db


def selecionarTodosRegistrosClimaticos():
    return db.session.execute(db.select(RegistrosClimaticos)).scalars().all()

def buscarRegistrosClimaticosPorId(id):
    return db.session.get(RegistrosClimaticos, id)

def inserirRegistrosClimaticos(Registro : RegistrosClimaticos):
    db.session.add(Registro)
    db.session.commit()
    db.session.refresh(Registro)
    return Registro

def alterarRegistrosClimaticos(Registro : RegistrosClimaticos):
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

        db.commit()

def deletarRegistrosClimaticos(id):
    reg = db.session.get(RegistrosClimaticos, id)

    if reg is not None:
        db.session.delete(reg)
        db.session.commit()