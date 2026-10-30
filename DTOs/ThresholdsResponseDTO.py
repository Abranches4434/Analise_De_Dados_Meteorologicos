from typing import TYPE_CHECKING

from pydantic import BaseModel

from Enum.TipoLimiar import TipoLimiar as TL
from Enum.Variavel import Variavel as Var
from Enum.Estacao import Estacao as Est

if TYPE_CHECKING:
    from Entity.Thresholds import Thresholds


class ThresholdsResponseDTO(BaseModel):

    IDThreshold: int

    FKLocalidade: int

    Variavel: Var

    TipoLimiar: TL

    EstacaoDoAno: Est

    Valor: float

    Ativo: bool

    @staticmethod
    def EntityToDTO(Threshold: "Thresholds") -> "ThresholdsResponseDTO":

        return ThresholdsResponseDTO(
            IDThreshold=Threshold.IDThreshold,
            FKLocalidade=Threshold.FKLocalidade,
            Variavel=Threshold.Variavel,
            TipoLimiar=Threshold.TipoLimiar,
            EstacaoDoAno=Threshold.EstacaoDoAno,
            Valor=Threshold.Valor,
            Ativo=Threshold.Ativo,
        )
