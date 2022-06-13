
from model import AutorArticulo


class pipe:
    def respuesta(resultado, estado):
        if(estado == 1):
            mensaje = {
                'codigo': 200,
                'mensaje': 'Accion exitosa se envia resultado',
                'respuesta': resultado
            }
        else:
            mensaje = {
                'codigo': 400,
                'mensaje': 'Hubo un error en el servicio',
                'respuesta': resultado
            }
        return mensaje

    def objToDict(objeto):
        array = []
        for item in objeto:
            temp = item.__dict__
            temp.pop('_sa_instance_state', None)
            array.append(temp)
        return array

    def relacion(array, id_articulo):
        temp = []
        for item in array:
            temp.append(AutorArticulo(id_articulo, item['identificacion']))
        return temp

    def libroConAutor(diccionario):
        print(diccionario)
        array  = []
        
