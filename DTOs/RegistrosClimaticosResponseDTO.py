from datetime import date, time
from pydantic import BaseModel

class RegistrosClimaticosReponseDTO(BaseModel):

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