from fastapi import FastAPI
from fastapi.responses import FileResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.libro import libro_router
from routers.categoria import categoria_router
from routers.user import user_router
from routers.http import http_router
from fastapi.staticfiles import StaticFiles 
import os

app = FastAPI()
app.title = "Mi primera chamba con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(libro_router)
app.include_router(categoria_router)
app.include_router(http_router) 

Base.metadata.create_all(bind=engine)

# Montar archivos estáticos
app.mount("/html", StaticFiles(directory="html"), name="html")


@app.get('/favicon.ico', tags=['home'])
def favicon():
    file_path = os.path.join(os.getcwd(), "html/favicon.ico")
    return FileResponse(file_path)


@app.get('/', tags=['home'])
def message():
    file_path = "html/index.html"
    return FileResponse(file_path)