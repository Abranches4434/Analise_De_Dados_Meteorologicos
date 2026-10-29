from pydantic import BaseModel, Field
from Enum.TipoLimiar import TipoLimiar as TL
from Enum.Variavel import Variavel as Var
from Enum.Estacao import Estacao as Est


class ThresholdsRequestDTO(BaseModel):

    FKLocalidade: int = Field()
    
    Variavel: Var = Field()
    
    TipoLimiar: TL = Field()
    
    EstacaoDoAno: Est = Field(default=Est.ANUAL)

    Valor: float = Field()

    Ativo: bool = Field()