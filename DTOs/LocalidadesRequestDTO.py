from pydantic import BaseModel, Field
from Enum.Estado import Estado

class LocalidadesRequestDTO(BaseModel):
    
    Nome: str = Field( min_length= 1, max_length=150)
    
    Cidade: str = Field( min_length= 1, max_length=150) 
    
    Estado: Estado
    
    Latitude: float = Field( ge= -90, le = 90) 
    
    Longitude: float = Field( ge = -180, le = 180)
    
    Ativo: bool