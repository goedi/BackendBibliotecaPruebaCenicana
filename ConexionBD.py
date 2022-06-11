from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class ConexionBD():
    conexion = None
    motor = 'postgresql'
    database = 'biblioteca'
    puerto = '5432'
    usuario = 'postgres'
    contrasenia = 'root'
    host = 'localhost'

    def __init__(self):
        engine = create_engine(self.motor + '://' + self.usuario + ':' + self.contrasenia + '@' + self.host + ':' + self.puerto + '/' + self.database)
        Session = sessionmaker(bind=engine)
        self.conexion = Session()
        print("la conexion fue exitosa")

    def getConexion(self):
        return (self.conexion)

    def cerrarConexion(self):
        self.conexion.close()
