from fastapi import Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.libro import Libro as LibroModel
from models.categoria import Categoria as CategoriaModel
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from services.libro import LibroService
from services.categoria import CategoriaService
from schemas.libro import Libro, LibroWithoutCodigo

libro_router = APIRouter()


@libro_router.get(
        '/libros',
        tags=['libros'],
        response_model=List[Libro],
        status_code=200
        )
def get_libros() -> List[Libro]:
    db = Session()
    result = LibroService(db).get_libros()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@libro_router.get(
        '/libros/{codigo}',
        tags=['libros'],
        response_model=Libro
        )

def get_libro(codigo: int = Path(ge=1, le=2000)) -> Libro:
    db = Session()
    result = LibroService(db).get_libro(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@libro_router.get(
        '/libros/categoria/',
        tags=['libros'],
        response_model=List[Libro]
        )
def get_libros_by_categoria(categoria: str = Query(max_length=15)):
    db = Session()
    if CategoriaService(db).get_categoria_by_nombre(categoria) is None:
        return JSONResponse(status_code=404, content={'message': "La categoria no existe"})
    result = LibroService(db).get_libros_by_categoria(categoria)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@libro_router.post(
        '/libros',
        tags=['libros'],
        response_model=dict,
        status_code=200
        )
def create_libro(libro: Libro) -> dict:
    db = Session()
    result = db.query(LibroModel).filter(
            LibroModel.codigo == libro.codigo).first()
    if result:
        return JSONResponse(status_code=403, content={'message': "Ese codigo ya esta ocupado"})
    result = db.query(CategoriaModel).filter(
            CategoriaModel.nombre == libro.categoria).first()
    if not result:
        return JSONResponse(status_code=403, content={'message': "La categoria no existe"})
    LibroService(db).create_libro(libro)
    return JSONResponse(status_code=200, content={"message": "Se ha registrado el libro"})


@libro_router.put(
        '/libros/{codigo}',
        tags=['libros'],
        response_model=dict,
        status_code=200
        )
def update_libro(codigo: int, libro: LibroWithoutCodigo) -> dict:
    db = Session()
    result = LibroService(db).get_libro(codigo)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    result = CategoriaService(db).get_categoria_by_nombre(libro.categoria)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Esta categoria no ha sido encontrada"})
    LibroService(db).update_libro(codigo, libro)
    return JSONResponse(status_code=202, content={'message': "Se ha modificado el libro"})


@libro_router.delete(
        '/libros/{codigo}',
        tags=['libros'],
        response_model=dict,
        status_code=200
        )
        
def delete_libro(codigo: int) -> dict:
    db = Session()
    result = db.query(LibroModel).filter(LibroModel.codigo == codigo).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    LibroService(db).delete_libro(codigo)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el libro"})
