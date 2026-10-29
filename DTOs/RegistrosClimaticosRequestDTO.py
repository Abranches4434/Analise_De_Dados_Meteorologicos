from pydantic import BaseModel, Field
from datetime import date, time

class RegistrosClimaticosRequestDTO(BaseModel):
    
    TempMax: float = Field(ge=-20, le=50)
    
    TempMin: float = Field(ge=-20, le=50)
    
    UmidadeRelativa: float = Field(ge=0, le=100)
    
    Precipitacao: float = Field(ge=0)
    
    VelocidadeVento: float = Field(ge=0)
    
    PressaoAtmosferica: float = Field(ge=0)
    
    Data: date = Field()
    
    Hora: time = Field()
    
    Ativo: bool = Field()
    
    FKLocalidade: int = Field()