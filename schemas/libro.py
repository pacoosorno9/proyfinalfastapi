from pydantic import BaseModel, Field
from typing import Optional


class Libro(BaseModel):
    codigo: Optional[int] = None
    titulo: str = Field(min_length=1, max_length=50)
    autor: str = Field(min_length=1, max_length=50)
    año: int = Field(lt=2024)
    categoria: str = Field(min_length=1)
    numPag: int = Field(gt=0)

    class Config:
        json_schema_extra = {
                "example": {
                    "codigo": 1,
                    "titulo": "The Raven",
                    "autor": "Edgar Allan Poe",
                    "año": 1845,
                    "categoria": "Terror",
                    "numPag": 54
                    }
                }


class LibroWithoutCodigo(BaseModel):
    titulo: str = Field(min_length=1, max_length=50)
    autor: str = Field(min_length=1, max_length=50)
    año: int = Field(lt=2024)
    categoria: str = Field(min_length=1)
    numPag: int = Field(gt=0)

    class Config:
        json_schema_extra = {
                "example": {
                    "titulo": "The Raven",
                    "autor": "Edgar Allan Poe",
                    "año": 1845,
                    "categoria": "Terror",
                    "numPag": 54
                    }
                }
