from models.libro import Libro as LibroModel
from models.categoria import Categoria as CategoriaModel
from services.categoria import CategoriaService
from schemas.libro import Libro


class LibroService():
    def __init__(self, db) -> None:
        self.db = db

    def get_libros(self):
        query = self.db.query(LibroModel).all()
        result = []
        for item in query:
            categoria = self.db.query(CategoriaModel).filter(CategoriaModel.codigo == item.codigoCategoria).first()
            result.append(
                    Libro(codigo=item.codigo,
                          titulo=item.titulo,
                          autor=item.autor,
                          año=item.año,
                          categoria=categoria.nombre,
                          numPag=item.numPag,
                          )
                    )
        return result

    def get_libro(self, codigo):
        query = self.db.query(LibroModel).filter(LibroModel.codigo == codigo).first()
        if query is None:
            return None
        categoria = self.db.query(CategoriaModel).filter(CategoriaModel.codigo == query.codigoCategoria).first()
        result = Libro(codigo=query.codigo,
                       titulo=query.titulo,
                       autor=query.autor,
                       año=query.año,
                       categoria=categoria.nombre,
                       numPag=query.numPag,
                       )
        return result

    def get_libros_by_categoria(self, categoria):
        categoriaObject = self.db.query(CategoriaModel).filter(CategoriaModel.nombre == categoria).first()
        query = self.db.query(LibroModel).filter(LibroModel.codigoCategoria == categoriaObject.codigo).all()
        result = []
        for item in query:
            result.append(
                    Libro(codigo=item.codigo,
                          titulo=item.titulo,
                          autor=item.autor,
                          año=item.año,
                          categoria=categoriaObject.nombre,
                          numPag=item.numPag,
                          )
                    )
        return result

    def create_libro(self, libro: Libro):
        query = CategoriaService(self.db).get_categoria_by_nombre(libro.categoria)
        new_libro = LibroModel(
                codigo=libro.codigo,
                titulo=libro.titulo,
                autor=libro.autor,
                año=libro.año,
                codigoCategoria=query.codigo,
                numPag=libro.numPag,
                )
        self.db.add(new_libro)
        self.db.commit()
        return

    def update_libro(self, codigo: int, data: Libro):
        libro = self.db.query(LibroModel).filter(LibroModel.codigo == codigo).first()
        categoria = self.db.query(CategoriaModel).filter(CategoriaModel.nombre == data.categoria).first()
        libro.titulo = data.titulo
        libro.autor = data.autor
        libro.año = data.año
        libro.codigoCategoria = categoria.codigo
        libro.numPag = data.numPag
        self.db.commit()
        return

    def delete_libro(self, codigo: int):
        self.db.query(LibroModel).filter(LibroModel.codigo == codigo).delete()
        self.db.commit()
        return
