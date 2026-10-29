from typing import TYPE_CHECKING

from pydantic import BaseModel, Field
from Enum.Estado import Estado

if TYPE_CHECKING:
    from Entity.Localidades import Localidades


class LocalidadesRequestDTO(BaseModel):

    IDLocalidade: int | None = None

    Nome: str = Field( min_length= 1, max_length=150)

    Cidade: str = Field( min_length= 1, max_length=150) 

    Estado: Estado

    Latitude: float = Field( ge= -90, le = 90) 

    Longitude: float = Field( ge = -180, le = 180)

    Ativo: bool = Field(default= True)

    def dtoToEntity(self) -> "Localidades":
        from Entity.Localidades import Localidades

        entity = Localidades()

        entity.IDLocalidade = self.IDLocalidade
        entity.Nome = self.Nome
        entity.Cidade = self.Cidade
        entity.Estado = self.Estado
        entity.Latitude = self.Latitude
        entity.Longitude = self.Longitude
        entity.Ativo = self.Ativo

        return entity
