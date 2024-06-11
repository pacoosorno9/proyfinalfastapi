from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Libro(Base):
    __tablename__ = "libros"

    codigo = Column(Integer, primary_key=True)
    titulo = Column(String)
    autor = Column(String)
    año = Column(Integer)
    codigoCategoria = Column(Integer, ForeignKey("categorias.codigo"))
    numPag = Column(Integer)
