from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, model_validator

from Enum.TipoLimiar import TipoLimiar as TL
from Enum.Variavel import Variavel as Var
from Enum.Estacao import Estacao as Est

if TYPE_CHECKING:
    from Entity.Thresholds import Thresholds


class ThresholdsRequestDTO(BaseModel):

    IDThreshold: int | None = None

    FKLocalidade: int = Field()

    Variavel: Var = Field()

    TipoLimiar: TL = Field()

    EstacaoDoAno: Est = Field(default=Est.ANUAL)

    Valor: float = Field()

    Ativo: bool = Field(default=True)

    @model_validator(mode="after")
    def validarRegras(self) -> "ThresholdsRequestDTO":

        if self.Variavel == Var.TEMPERATURA:
            if self.TipoLimiar not in (TL.MAXIMO, TL.MINIMO):
                raise ValueError("Temperatura aceita apenas os tipos de limiar MAXIMO ou MINIMO!")
            if not -20 <= self.Valor <= 50:
                raise ValueError("O valor do limiar de temperatura deve estar entre -20 e 50!")

        elif self.Variavel == Var.UMIDADE:
            if self.TipoLimiar not in (TL.MAXIMO, TL.MINIMO):
                raise ValueError("Umidade aceita apenas os tipos de limiar MAXIMO ou MINIMO!")
            if not 0 <= self.Valor <= 100:
                raise ValueError("O valor do limiar de umidade deve estar entre 0 e 100!")

        elif self.Variavel == Var.PRECIPITACAO:
            if self.Valor < 0:
                raise ValueError("O valor do limiar de precipitação não pode ser negativo!")
            if self.TipoLimiar == TL.DIASSEMCHUVA and not float(self.Valor).is_integer():
                raise ValueError("O limiar DIASSEMCHUVA deve ser um número inteiro de dias!")

        elif self.Variavel in (Var.VELOCIDADEVENTO, Var.PRESSAOATMOSFERICA):
            if self.TipoLimiar not in (TL.MAXIMO, TL.MINIMO):
                raise ValueError("Essa variável aceita apenas os tipos de limiar MAXIMO ou MINIMO!")
            if self.Valor < 0:
                raise ValueError("O valor do limiar não pode ser negativo!")

        return self

    def dtoToEntity(self) -> "Thresholds":
        from Entity.Thresholds import Thresholds

        entity = Thresholds()

        entity.IDThreshold = self.IDThreshold
        entity.FKLocalidade = self.FKLocalidade
        entity.Variavel = self.Variavel
        entity.TipoLimiar = self.TipoLimiar
        entity.EstacaoDoAno = self.EstacaoDoAno
        entity.Valor = self.Valor
        entity.Ativo = self.Ativo

        return entity
