from Entity import db
from Enum.Estado import Estado


class Localidades(db.Model):
    __tablename__ = "Localidades"

    IDLocalidade = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(150), nullable=False)
    Cidade = db.Column(db.String(150), nullable=False)
    Estado = db.Column(db.Enum(Estado), nullable=False)
    Latitude = db.Column(db.Numeric(8, 6), db.CheckConstraint("Latitude >= -90 and Latitude <= 90"), nullable=False)
    Longitude = db.Column(db.Numeric(9, 6), db.CheckConstraint("Longitude >= -180 and Longitude <= 180"), nullable=False)
    Ativo = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        db.UniqueConstraint(
            "Latitude",
            "Longitude",
            name="uq_localidades_latitude_longitude"
        ),
    )
