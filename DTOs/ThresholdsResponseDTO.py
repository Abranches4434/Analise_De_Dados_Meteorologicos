from pydantic import BaseModel
from Enum.TipoLimiar import TipoLimiar as TL
from Enum.Variavel import Variavel as Var
from Enum.Estacao import Estacao as Est

class ThresholdsResponseDTO(BaseModel):

    IDThreshold: int   

    FKLocalidade: int
    
    Variavel: Var
    
    TipoLimiar: TL
    
    EstacaoDoAno: Est

    Valor: float

    Ativo: bool