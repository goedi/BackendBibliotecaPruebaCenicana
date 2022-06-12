from model import Libro, Autor, Articulo
from ConexionBD import *

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
        productos = db.getConexion().query(Autor).all()
        db.cerrarConexion()
        return productos
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
    productos = db.getConexion().query(Libro).all()
    db.cerrarConexion()
    return productos

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
    carrito = db.getConexion().query(Articulo).all()
    db.cerrarConexion()
    return carrito


def crearAsociacion(autor_articulo):
    db = ConexionBD()
    db.getConexion().add_all(autor_articulo)
    db.getConexion().commit()
    db.cerrarConexion()