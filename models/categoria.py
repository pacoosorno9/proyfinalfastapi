from config.database import Base
from sqlalchemy import Column, Integer, String


class Categoria(Base):
    __tablename__ = "categorias"

    codigo = Column(Integer, primary_key=True)
    nombre = Column(String)