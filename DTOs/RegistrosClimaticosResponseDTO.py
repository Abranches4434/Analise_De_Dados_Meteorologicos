from datetime import date, time
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from Entity.RegistrosClimaticos import RegistrosClimaticos


class RegistrosClimaticosResponseDTO(BaseModel):

    IDRegistrosClimaticos: int

    TempMax: float

    TempMin: float

    UmidadeRelativa: float

    Precipitacao: float

    VelocidadeVento: float

    PressaoAtmosferica: float

    Data: date

    Hora: time

    Ativo: bool

    FKLocalidade: int

    @staticmethod
    def EntityToDTO(Registro: "RegistrosClimaticos") -> "RegistrosClimaticosResponseDTO":

        return RegistrosClimaticosResponseDTO(
            IDRegistrosClimaticos=Registro.IDRegistrosClimaticos,
            TempMax=Registro.TempMax,
            TempMin=Registro.TempMin,
            UmidadeRelativa=Registro.UmidadeRelativa,
            Precipitacao=Registro.Precipitacao,
            VelocidadeVento=Registro.VelocidadeVento,
            PressaoAtmosferica=Registro.PressaoAtmosferica,
            Data=Registro.Data,
            Hora=Registro.Hora,
            Ativo=Registro.Ativo,
            FKLocalidade=Registro.FKLocalidade,
        )
