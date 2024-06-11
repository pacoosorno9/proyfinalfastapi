from fastapi import Path
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.categoria import Categoria as CategoriaModel
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from services.categoria import CategoriaService
from services.libro import LibroService
from schemas.categoria import Categoria, CategoriaWithoutCodigo

categoria_router = APIRouter()


@categoria_router.get(
        '/categorias',
        tags=['categorias'],
        response_model=List[Categoria],
        status_code=200
        )
def get_categorias() -> List[Categoria]:
    db = Session()
    result = CategoriaService(db).get_categorias()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@categoria_router.get(
        '/categorias/{codigo}',
        tags=['categorias'],
        response_model=Categoria
        )
# def get_categoria(codigo: int = Path(ge=1, le=2000)) -> Categoria:
def get_categoria(codigo: int = Path(ge=1)) -> Categoria:
    db = Session()
    result = CategoriaService(db).get_categoria(codigo)
    if not result:
        return JSONResponse(status_code=404,
                            content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@categoria_router.get(
        '/categorias/nombre/',
        tags=['categorias'],
        response_model=Categoria
        )
def get_categoria_by_nombre(nombre: str) -> Categoria:
    db = Session()
    result = CategoriaService(db).get_categoria_by_nombre(nombre)
    if not result:
        return JSONResponse(status_code=404,
                            content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@categoria_router.post(
        '/categorias',
        tags=['categorias'],
        response_model=dict,
        status_code=200
        )
def create_categoria(categoria: Categoria) -> dict:
    db = Session()
    result = db.query(CategoriaModel).filter(
            CategoriaModel.codigo == categoria.codigo).first()
    if result:
        return JSONResponse(
                status_code=403,
                content={'message': "Ese codigo ya esta ocupado"})
    result = db.query(CategoriaModel).filter(
            CategoriaModel.nombre == categoria.nombre).first()
    if result:
        return JSONResponse(
                status_code=403,
                content={'message': "Esa categoria ya existe"})
    CategoriaService(db).create_categoria(categoria)
    return JSONResponse(
            status_code=200,
            content={"message": "Se ha registrado la categoria"})


@categoria_router.put(
        '/categorias/{codigo}',
        tags=['categorias'],
        response_model=dict,
        status_code=200
        )
def update_categoria(codigo: int, categoria: CategoriaWithoutCodigo) -> dict:
    db = Session()
    result = CategoriaService(db).get_categoria(codigo)
    if not result:
        return JSONResponse(
                status_code=404,
                content={'message': "No encontrado"})
    result = db.query(CategoriaModel).filter(
            CategoriaModel.nombre == categoria.nombre).first()
    if result:
        return JSONResponse(
                status_code=403,
                content={'message': "Esa categoria ya existe"})
    CategoriaService(db).update_categoria(codigo, categoria)
    return JSONResponse(
            status_code=202,
            content={'message': "Se ha modificado el categoria"})


@categoria_router.delete(
        '/categorias/{codigo}',
        tags=['categorias'],
        response_model=dict,
        status_code=200
        )
def delete_categoria(codigo: int) -> dict:
    db = Session()
    result = db.query(CategoriaModel).filter(
            CategoriaModel.codigo == codigo).first()
    if not result:
        return JSONResponse(
                status_code=404,
                content={'message': "La categoria no existe"})
    if LibroService(db).get_libros_by_categoria(result.nombre) != []:
        return JSONResponse(
                status_code=404,
                content={'message': "Hay libros bajo esa categoria"})
    CategoriaService(db).delete_categoria(codigo)
    return JSONResponse(
            status_code=200,
            content={"message": "Se ha eliminado el categoria"})
