from models.categoria import Categoria as CategoriaModel
from schemas.categoria import Categoria


class CategoriaService():
    def __init__(self, db) -> None:
        self.db = db

    def get_categorias(self):
        result = self.db.query(CategoriaModel).all()
        return result

    def get_categoria(self, codigo):
        result = self.db.query(CategoriaModel).filter(CategoriaModel.codigo == codigo).first()
        return result

    def get_categoria_by_nombre(self, nombre):
        result = self.db.query(CategoriaModel).filter(CategoriaModel.nombre == nombre).first()
        return result

    def create_categoria(self, categoria: Categoria):
        new_categoria = CategoriaModel(**categoria.model_dump())
        self.db.add(new_categoria)
        self.db.commit()
        return

    def update_categoria(self, codigo: int, data: Categoria):
        categoria = self.db.query(CategoriaModel).filter(CategoriaModel.codigo == codigo).first()
        categoria.nombre = data.nombre
        self.db.commit()
        return

    def delete_categoria(self, codigo: int):
        self.db.query(CategoriaModel).filter(CategoriaModel.codigo == codigo).delete()
        self.db.commit()
        return
