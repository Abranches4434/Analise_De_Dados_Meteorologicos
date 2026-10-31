from datetime import date, time
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, model_validator

if TYPE_CHECKING:
    from Entity.RegistrosClimaticos import RegistrosClimaticos


class RegistrosClimaticosRequestDTO(BaseModel):

    IDRegistrosClimaticos: int | None = None

    TempMax: float = Field(ge=-20, le=50)

    TempMin: float = Field(ge=-20, le=50)

    TempMedia: float = Field(ge=-20, le=50)

    UmidadeRelativa: float = Field(ge=0, le=100)

    Precipitacao: float = Field(ge=0)

    VelocidadeVento: float = Field(ge=0, le=150)

    PressaoAtmosferica: float = Field(ge=800, le=1100)

    Data: date = Field()

    Hora: time = Field()

    Ativo: bool = Field(default=True)

    FKLocalidade: int = Field()

    @model_validator(mode="after")
    def validarRegras(self) -> "RegistrosClimaticosRequestDTO":

        if self.TempMin > self.TempMax:
            raise ValueError("A temperatura mínima não pode ser maior que a temperatura máxima!")

        if not self.TempMin <= self.TempMedia <= self.TempMax:
            raise ValueError(
                "A temperatura média deve estar entre a temperatura mínima e a máxima!"
            )

        if self.Data > date.today():
            raise ValueError("A data do registro não pode ser futura!")

        return self

    def dtoToEntity(self) -> "RegistrosClimaticos":
        from Entity.RegistrosClimaticos import RegistrosClimaticos

        entity = RegistrosClimaticos()

        entity.IDRegistrosClimaticos = self.IDRegistrosClimaticos
        entity.TempMax = self.TempMax
        entity.TempMin = self.TempMin
        entity.TempMedia = self.TempMedia
        entity.UmidadeRelativa = self.UmidadeRelativa
        entity.Precipitacao = self.Precipitacao
        entity.VelocidadeVento = self.VelocidadeVento
        entity.PressaoAtmosferica = self.PressaoAtmosferica
        entity.Data = self.Data
        entity.Hora = self.Hora
        entity.Ativo = self.Ativo
        entity.FKLocalidade = self.FKLocalidade

        return entity
