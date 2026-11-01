from Entity import db


class RegistrosClimaticos(db.Model):
    __tablename__ = "RegistrosClimaticos"

    IDRegistrosClimaticos = db.Column(db.Integer, primary_key=True)
    TempMax = db.Column(
        db.Numeric(4, 1),
        db.CheckConstraint('"TempMax" between -20 and 50'),
        nullable=False,
    )
    TempMin = db.Column(
        db.Numeric(4, 1),
        db.CheckConstraint('"TempMin" between -20 and 50'),
        nullable=False,
    )
    TempMedia = db.Column(
        db.Numeric(4, 1),
        db.CheckConstraint('"TempMedia" between -20 and 50'),
        nullable=False,
    )
    UmidadeRelativa = db.Column(
        db.Numeric(5, 2),
        db.CheckConstraint('"UmidadeRelativa" between 0 and 100'),
        nullable=False,
    )
    Precipitacao = db.Column(
        db.Numeric(5, 2),
        db.CheckConstraint('"Precipitacao" >= 0'),
        nullable=False,
    )
    VelocidadeVento = db.Column(
        db.Numeric(5, 2),
        db.CheckConstraint('"VelocidadeVento" between 0 and 150'),
        nullable=False,
    )
    PressaoAtmosferica = db.Column(
        db.Numeric(7, 2),
        db.CheckConstraint('"PressaoAtmosferica" between 800 and 1100'),
        nullable=False,
    )
    Data = db.Column(db.Date, nullable=False)
    Hora = db.Column(db.Time, nullable=False)
    Ativo = db.Column(db.Boolean, nullable=False, default=True)
    FKLocalidade = db.Column(db.Integer, db.ForeignKey("Localidades.IDLocalidade", ondelete="no action"), nullable=False)

    localidade = db.relationship(
        "Localidades",
        back_populates="registros",
        lazy="select",
    )

    __table_args__ = (
        db.CheckConstraint(
            '"TempMin" <= "TempMax"',
            name="ck_registros_tempmin_tempmax",
        ),
        db.CheckConstraint(
            '"TempMin" <= "TempMedia" and "TempMedia" <= "TempMax"',
            name="ck_registros_tempmin_tempmedia_tempmax",
        ),
        db.UniqueConstraint(
            "Data",
            "Hora",
            "FKLocalidade",
            name="uq_registros_data_hora_localidade"
        ),
    )
