from pydantic import BaseModel
from Enum.Estado import Estado

class LocalidadesResponseDTO(BaseModel):

    IDLocalidade: int

    Nome: str
    
    Cidade: str 
    
    Estado: Estado
    
    Latitude: float 
    
    Longitude: float 
    
    Ativo: bool