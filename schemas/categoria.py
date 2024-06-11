from pydantic import BaseModel, Field
from typing import Optional


class Categoria(BaseModel):
    codigo: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=50)

    class Config:
        json_schema_extra = {
                "example": {
                    "codigo": 1,
                    "nombre": "Terror",
                    }
                }


class CategoriaWithoutCodigo(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)

    class Config:
        json_schema_extra = {
                "example": {
                    "nombre": "Terror",
                    }
                }
