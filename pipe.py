from asyncio.windows_events import NULL
from curses.ascii import NUL


class pipe:
    def respuesta(resultado, estado):
        if(estado == 1):
            mensaje = {
                'codigo': 200,
                'mensaje': 'Acción exitosa se envia resultado',
                'respuesta': resultado
            }
        else:
            mensaje = {
                'codigo': 400,
                'mensaje': 'Hubo un error en el servicio',
                'respuesta': NULL
            }
        return mensaje

    def objToDict(objeto):
        array = []
        for item in objeto:
            temp = item.__dict__
            temp.pop('_sa_instance_state', None)
            array.append(temp)
        return array


