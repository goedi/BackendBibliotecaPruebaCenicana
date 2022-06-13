from model import AutorArticulo, Libro, Autor, Articulo
from sqlalchemy import and_, desc
from sqlalchemy.sql import select, update
from ConexionBD import *
from pipe import pipe

# *************************************************************************
# *************************************************************************
# *************************************************************************


def crearAutor(autor):
    try:
        db = ConexionBD()
        db.getConexion().add(autor)
        db.getConexion().commit()
        db.cerrarConexion()
    except Exception as err:
        print(err.args)


def listarAutores():
    try:
        db = ConexionBD()
        autores = db.getConexion().query(Autor).all()
        db.cerrarConexion()
        return autores
    except TypeError as err:
        print(err.args)
        return None


# *************************************************************************
# *************************************************************************
# *************************************************************************
def crearLibro(libro):
    db = ConexionBD()
    db.getConexion().add(libro)
    db.getConexion().commit()
    db.cerrarConexion()


def listarLibros():
    db = ConexionBD()
    query = select([Libro, Autor]).where(
        and_(Autor.identificacion == Libro.id_autor,
             Libro.estado == True))

    result = db.getConexion().execute(query)

    array = []
    for row in result:
        libro_autor = pipe.objToDict(row)
        libro = libro_autor[0]
        libro['id_autor'] = libro_autor[1]
        array.append(libro)

    db.cerrarConexion()
    return array


def buscarUnLibro(isbn):
    db = ConexionBD()
    query = select([Libro, Autor]).where(
        and_(Autor.identificacion == Libro.id_autor,
             Libro.ISBN == isbn))

    result = db.getConexion().execute(query)

    array = []
    for row in result:
        libro_autor = pipe.objToDict(row)
        libro = libro_autor[0]
        libro['id_autor'] = libro_autor[1]
        array.append(libro)

    db.cerrarConexion()
    return array


def updateLibro(libro):
    db = ConexionBD()
    query = update(Libro).where(Libro.ISBN == libro.ISBN).values(
        fecha_publicacion=libro.fecha_publicacion,
        id_autor=libro.id_autor,
        idioma_original=libro.idioma_original,
        titulo=libro.titulo
    )
    db.getConexion().execute(query)
    db.getConexion().commit()
    db.cerrarConexion()


def deleteLibro(libro):
    db = ConexionBD()
    query = update(Libro).where(
        Libro.ISBN == libro.ISBN).values(
        estado=False)

    db.getConexion().execute(query)
    db.getConexion().commit()
    db.cerrarConexion()

    
# *************************************************************************
# *************************************************************************
# *************************************************************************


def crearArticulo(articulo):
    db = ConexionBD()
    db.getConexion().add(articulo)
    db.getConexion().commit()
    db.cerrarConexion()


def listarArticulos():
    db = ConexionBD()
    result = db.getConexion().query(Articulo).all()

    result = pipe.objToDict(result)

    array = []
    for row in result:
        articulo = row
        articulo['autores'] = autores_articulo(row)
        array.append(articulo)
    db.cerrarConexion()

    return array


def autores_articulo(issn):
    db = ConexionBD()
    query = select([Autor]).where(and_(AutorArticulo.id_articulo == issn['issn'],
                                       Autor.identificacion == AutorArticulo.id_autor))
    result = db.getConexion().execute(query)
    array = []
    for fila in result:
        fila = pipe.objToDict(fila)
        print(type(fila))
        array.append(fila[0])
    db.cerrarConexion()
    return array


def crearAsociacion(autor_articulo):
    db = ConexionBD()
    db.getConexion().add_all(autor_articulo)
    db.getConexion().commit()
    db.cerrarConexion()
