from Entity import db
from Enum.Variavel import Variavel
from Enum.TipoLimiar import TipoLimiar
from Enum.Estacao import Estacao


class Thresholds(db.Model):
    __tablename__ = "Thresholds"

    IDThreshold = db.Column(db.Integer, primary_key=True)
    FKLocalidade = db.Column(db.Integer, db.ForeignKey("Localidades.IDLocalidade", ondelete="no action"), nullable=False)
    Variavel = db.Column(db.Enum(Variavel), nullable=False)
    TipoLimiar = db.Column(db.Enum(TipoLimiar), nullable=False)
    EstacaoDoAno = db.Column(db.Enum(Estacao), nullable=False, default=Estacao.ANUAL)
    Valor = db.Column(db.Numeric(7, 2), nullable=False)
    Ativo = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        db.UniqueConstraint(
            "FKLocalidade",
            "Variavel",
            "TipoLimiar",
            "EstacaoDoAno",
            name="uq_thresholds_localidade_variavel_tipo_estacao"
        ),
    )
