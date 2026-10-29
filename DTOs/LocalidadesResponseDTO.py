from typing import TYPE_CHECKING

from pydantic import BaseModel
from Enum.Estado import Estado as Est

if TYPE_CHECKING:
    from Entity.Localidades import Localidades


class LocalidadesResponseDTO(BaseModel):

    IDLocalidade: int

    Nome: str
    
    Cidade: str 
    
    Estado: Est
    
    Latitude: float 
    
    Longitude: float 
    
    Ativo: bool

    @staticmethod
    def EntityToDTO(Localidade: "Localidades") -> "LocalidadesResponseDTO":

        return LocalidadesResponseDTO(IDLocalidade= Localidade.IDLocalidade
                                     ,Nome= Localidade.Nome
                                     ,Cidade= Localidade.Cidade
                                     ,Estado= Localidade.Estado
                                     ,Latitude= Localidade.Latitude
                                     ,Longitude= Localidade.Longitude
                                     ,Ativo= Localidade.Ativo)
