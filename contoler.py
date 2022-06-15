from model import AutorArticulo, Libro, Autor, Articulo
from sqlalchemy import and_, desc, text
from sqlalchemy.sql import select, update, delete
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
        err


def listarAutores():
    try:
        db = ConexionBD()
        autores = db.getConexion().query(Autor).all()
        db.cerrarConexion()
        return autores
    except TypeError as err:
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
    query = select(Articulo).where(Articulo.estado == True)

    result = db.getConexion().execute(query)

    array = []
    for row in result:
        articulo = pipe.objToDict(row)
        articulo = articulo[0]
        articulo['autores'] = autores_articulo(articulo)
        array.append(articulo)
    db.cerrarConexion()
    return array


def buscarUnArticulo(issn):
    db = ConexionBD()
    query = select(Articulo).where(Articulo.issn == issn)
    result = db.getConexion().execute(query)

    array = []
    for row in result:
        articulo = pipe.objToDict(row)
        articulo = articulo[0]
        articulo['autores'] = autores_articulo(articulo)
        array.append(articulo)

    db.cerrarConexion()
    return array


def autores_articulo(articulo):
    db = ConexionBD()
    query = select([Autor]
                   ).where(and_(AutorArticulo.id_articulo == articulo['issn'],
                                Autor.identificacion == AutorArticulo.id_autor))
    result = db.getConexion().execute(query)
    array = []
    for fila in result:
        fila = pipe.objToDict(fila)
        array.append(fila[0])
    db.cerrarConexion()
    return array


def updateArticulo(articulo, autores):
    db = ConexionBD()
    query = update(Articulo).where(Articulo.issn == articulo.issn).values(
        fecha_publicacion=articulo.fecha_publicacion,
        titulo=articulo.titulo,
        paginas=articulo.paginas,
        publicacion=articulo.publicacion,
        resumen=articulo.resumen,
    )
    EliminarAsociacion(articulo.issn)
    crearAsociacion(pipe.relacion(autores, articulo.issn))

    db.getConexion().execute(query)
    db.getConexion().commit()
    db.cerrarConexion()


def deleteArticulo(articulo):
    db = ConexionBD()
    query = update(Articulo).where(
        Articulo.issn == articulo.issn).values(
        estado=False)

    db.getConexion().execute(query)
    db.getConexion().commit()
    db.cerrarConexion()


def crearAsociacion(autor_articulo):
    db = ConexionBD()
    db.getConexion().add_all(autor_articulo)
    db.getConexion().commit()
    db.cerrarConexion()


def EliminarAsociacion(issn):
    db = ConexionBD()
    query = delete(AutorArticulo).where(AutorArticulo.id_articulo == issn)
    db.getConexion().execute(query)
    db.getConexion().commit()
    db.cerrarConexion()


# *************************************************************************
# *************************************************************************
# *************************************************************************

def publicacionLibros(id):
    db = ConexionBD()
    array = []
    query = text("select issn  as codigo, " +
                 "titulo as titulo, " +
                 "fecha_publicacion as fecha, " +
                 "identificacion id_autor, " +
                 "(nombres || ' ' || apellidos) autor, " +
                 "'articulo' as tipo " +
                 "from articulo "
                 " join autor_articulo on id_articulo=issn "
                 " join autor on id_autor=identificacion "
                 "where autor.estado=true and identificacion='" + id + "';")
    result = db.getConexion().execute(query)
    for item in result:
        temp = {'codigo': item[0], 'titulo': item[1],
                'fecha': item[2], 'tipo': item[5], 'id_autor': item[3], 'autor': item[4]}
        array.append(temp)

    db.cerrarConexion()
    return array


def publicacionArticulos(id):
    db = ConexionBD()
    query = text('select li."ISBN"  as codigo, ' +
                 "li.titulo as titulo, " +
                 "li.fecha_publicacion as fecha," +
                 " a.identificacion id_autor, " +
                 " (a.nombres || ' ' || a.apellidos) autor, " +
                 " 'libro' as tipo " +
                 " from libro as li " +
                 "join autor a on a.identificacion=li.id_autor " +
                 "where li.estado=true " +
                 "and li.id_autor='" + id + "';")
    result = db.getConexion().execute(query)

    array = []
    for item in result:
        temp = {'codigo': item[0], 'titulo': item[1],
                'fecha': item[2], 'tipo': item[5], 'id_autor': item[3], 'autor': item[4]}
        array.append(temp)

    db.cerrarConexion()
    return array


def totalLibro():
    db = ConexionBD()
    query = text("select count(extract(year from libro.fecha_publicacion)) total, " +
                 "extract(year from libro.fecha_publicacion) año, " +
                 "(autor.nombres || ' ' || autor.apellidos) autor, " +
                 "autor.identificacion id_autor "
                 "from libro join autor on autor.identificacion = libro.id_autor " +
                 "group by autor.identificacion, libro.fecha_publicacion, autor.nombres, autor.apellidos;")
    result = db.getConexion().execute(query)

    array = []
    for item in result:
        temp = {'total': item[0], 'año': item[1],
                'autor': item[2], 'id_autor': item[3], 'tipo': 'libro'}
        array.append(temp)

    db.cerrarConexion()
    return array


def totalArticulos():
    db = ConexionBD()
    query = text("select count(extract(year from ar.fecha_publicacion)) total, " +
                 "extract(year from ar.fecha_publicacion) año, " +
                 "(a.nombres || ' ' || a.apellidos) autor, " +
                 " a.identificacion id_autor " +
                 " from articulo as ar " +
                 "join autor_articulo aa on aa.id_articulo=ar.issn " +
                 "join autor a on aa.id_autor=a.identificacion " +
                 "group by a.identificacion, extract(year from ar.fecha_publicacion), a.nombres, a.apellidos")
    result = db.getConexion().execute(query)

    array = []
    for item in result:
        temp = {'total': item[0], 'año': item[1],
                'autor': item[2], 'id_autor': item[3], 'tipo':'articulo'}
        array.append(temp)

    db.cerrarConexion()
    return array


def autoresPublicaron():
    db = ConexionBD()
    query = text("select autor.* from autor join libro on autor.identificacion = libro.id_autor " +
                 "union " +
                 "select autor.* from autor join autor_articulo aa on autor.identificacion =aa.id_autor;")
    result = db.getConexion().execute(query)

    array = []
    for item in result:
        temp = {'identificacion': item[0],
                'nombres': item[1],
                'apellidos': item[2], 
                'biografia': item[3],
                'fecha_nacimiento': item[4],
                'fecha_muerte': item[5],
                'ruta_img': item[6],
                'estado': item[7]}
        array.append(temp)

    db.cerrarConexion()
    return array
