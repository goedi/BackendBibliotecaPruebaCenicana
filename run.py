from contoler import *
from flask import request
from flask import Flask, jsonify
from flask_cors import CORS
from model import Articulo, Autor, Libro
from pipe import pipe

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# *************************************************************************
# *************************************************************************
# *************************************************************************


@app.route("/api/autor/list", methods=['GET'])
def listadoAutores():
    array = listarAutores()
    if len(array) > 0:
        return pipe.respuesta(pipe.objToDict(array), 1)
    else:
        return pipe.respuesta(None, -1)


@app.route("/api/autor/create", methods=['POST'])
def autorCreate():
    data = request.json
    autor = Autor(data['identificacion'], data['nombres'], data['apellidos'],
                  data['biografia'], data['fecha_nacimiento'], data['fecha_muerte'],
                  data['ruta_img'], data['estado'])
    crearAutor(autor)
    response = 'se creo el autor con exito'

    return pipe.respuesta(response, 1)


# *************************************************************************
# *************************************************************************
# *************************************************************************
@app.route("/api/libro/list", methods=['GET'])
def libroList():
    array = listarLibros()

    if len(array) > 0:
        return pipe.respuesta(array, 1)
    else:
        return pipe.respuesta(None, -1)


@app.route("/api/libro/create", methods=['POST'])
def LibroCreate():
    data = request.json

    libro = Libro(data['ISBN'], data['titulo'], data['fecha_publicacion'],
                  data['idioma_original'], data['resumen'], data['id_autor']['identificacion'],
                  data['estado'])

    crearLibro(libro)
    response = 'se creo el libro con exito'

    return pipe.respuesta(response, 1)


@app.route("/api/libro/buscar/<isbn>", methods=['GET'])
def buscarLibro(isbn):
    array = buscarUnLibro(isbn)
    if len(array) > 0:
        return pipe.respuesta(array, 1)
    else:
        return pipe.respuesta(None, -1)


@app.route("/api/libro/update", methods=['POST'])
def actualizarLibro():
    data = request.json
    libro = Libro(data['ISBN'], data['titulo'], data['fecha_publicacion'],
                  data['idioma_original'], data['resumen'], data['id_autor']['identificacion'],
                  data['estado'])
    updateLibro(libro)
    return pipe.respuesta('respuesta ok', 1)


@app.route("/api/libro/delete", methods=['POST'])
def eliminarLibro():
    data = request.json
    libro = Libro(data['ISBN'], data['titulo'], data['fecha_publicacion'],
                  data['idioma_original'], data['resumen'], data['id_autor']['identificacion'],
                  data['estado'])
    deleteLibro(libro)
    return pipe.respuesta('respuesta ok', 1)


# *************************************************************************
# *************************************************************************
# *************************************************************************


@app.route("/api/articulo/list", methods=['GET'])
def articuloList():
    array = listarArticulos()
    if len(array) > 0:
        return pipe.respuesta(array, 1)
    else:
        return pipe.respuesta(None, -1)


@app.route("/api/articulo/buscar/<issn>", methods=['GET'])
def buscarArticulo(issn):
    array = buscarUnArticulo(issn)
    if len(array) > 0:
        return pipe.respuesta(array, 1)
    else:
        return pipe.respuesta(None, -1)


@app.route("/api/articulo/create", methods=['POST'])
def articuloCreate():
    data = request.json
    dataAutor = data['autores']

    articulo = Articulo(data['titulo'], data['issn'], data['paginas'],
                        data['fecha_publicacion'], data['publicacion'], data['resumen'],
                        data['estado'])
    crearArticulo(articulo)
    crearAsociacion(pipe.relacion(dataAutor, data['issn']))

    response = 'se creo el Articulo con exito'

    return pipe.respuesta(response, 1)


@app.route("/api/articulo/update", methods=['POST'])
def articuloUpdate():
    data = request.json

    dataAutor = data['autores']
    print('llega', data)
    articulo = Articulo(data['titulo'], data['issn'], data['paginas'],
                        data['fecha_publicacion'], data['publicacion'], data['resumen'],
                        data['estado'])
    print('route', articulo)
    updateArticulo(articulo, dataAutor)
    response = 'se actuallizo el Articulo con exito'

    return pipe.respuesta(response, 1)


@app.route("/api/articulo/delete", methods=['POST'])
def eliminarArticulo():
    data = request.json
    articulo = Articulo(data['titulo'], data['issn'], data['paginas'],
                        data['fecha_publicacion'], data['publicacion'], data['resumen'],
                        data['estado'])
    deleteArticulo(articulo)
    return pipe.respuesta('respuesta ok', 1)

# *************************************************************************
# *************************************************************************
# *************************************************************************


@app.route("/api/autor/con_publicaciones", methods=["GET"])
def autoresConPublicaciones():
    array = []
    array = autoresPublicaron()
    return pipe.respuesta(array, 1)

@app.route("/api/autor/publicaciones/<id>", methods=["GET"])
def publicaciones(id):
    array = []
    array = publicacionLibros(id)
    array2 = publicacionArticulos(id)
    for r in array2:
        array.append(r)

    return pipe.respuesta(array, 1)


@app.route("/api/autor/total_publicaciones", methods=["GET"])
def totalPublicaciones():
    array = []
    array = totalLibro()
    array2 = totalArticulos()
    for r in array2:
        array.append(r)

    return pipe.respuesta(array, 1)


if __name__ == "__main__":
    app.run(debug=True)
