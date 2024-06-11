from fastapi.responses import FileResponse
import os
from fastapi import APIRouter

http_router = APIRouter()


@http_router.get('/categorias.html', tags=['home'])
def categorias():
    file_path = os.path.join(os.getcwd(), "html/ver_categorias.html")
    return FileResponse(file_path)


@http_router.get('/libros.html', tags=['home'])
def peliculas():
    file_path = os.path.join(os.getcwd(), "html/ver_libros.html")
    return FileResponse(file_path)