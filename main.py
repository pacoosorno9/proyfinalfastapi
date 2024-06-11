from fastapi import FastAPI
from fastapi.responses import FileResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.libro import libro_router
from routers.categoria import categoria_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "Mi primera chamba"

# Configuración de CORS
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5500",  # Cambia el puerto si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandler)
app.include_router(libro_router)
app.include_router(categoria_router)

Base.metadata.create_all(bind=engine)

# Montar archivos estáticos
app.mount("/html", StaticFiles(directory="html"), name="html")

@app.get('/', tags=['home'])
def message():
    file_path = "html/index.html"
    return FileResponse(file_path)
