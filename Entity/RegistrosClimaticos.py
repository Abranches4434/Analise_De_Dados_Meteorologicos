from Entity import db


class RegistrosClimaticos(db.Model):
        __tablename__ = "RegistrosClimaticos"

        IDRegistrosClimaticos = db.Column(db.Integer, primary_key = True)
        TempMax = db.Column(db.Numeric(4,1), db.CheckConstraint("TempMax between -20 and 50"))
        TempMin = db.Column(db.Numeric(4,1), db.CheckConstraint("TempMin between -20 and 50 and TempMin <= TempMax"))
        UmidadeRelativa = db.Column(db.Numeric(3,2), db.CheckConstraint("UmidadeRelativa between 0 and 100"))
        Precipitacao = db.Column(db.Numeric(5,2), db.CheckConstraint("Precipitacao >= 0"))
        VelocidadeVento = db.Column(db.Numeric(5,2), db.CheckConstraint("VelocidadeVento >= 0"))
        PressaoAtmosferica = db.Column(db.Numeric(4,2), db.CheckConstraint("PressaoAtmosferica >= 0"))
        Data = db.Column(db.Date)
        Hora = db.Column(db.Time)
        Ativo = db.Column(db.Boolean)
        FKLocalidade = db.Column(db.Integer, db.ForeignKey("Localidades.IDLocalidade", ondelete = "no action") , nullable = False)

        __table_args__ = (
                db.UniqueConstraint(
                        "Data",
                        "Hora",
                        "FKLocalidade"
                ),
        )
