from msilib import sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Sequence, Date, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import null

Base = declarative_base()


class Autor(Base):
    __tablename__ = 'autor'
    identificacion = Column(String, primary_key=True)
    nombres = Column(String(60))
    apellidos = Column(String(60))
    biografia = Column(String)
    fecha_nacimiento = Column(Date)
    fecha_muerte = Column(Date)
    ruta_img = Column(String(200))

    def __init__(self, identificacion, nombres,  apellidos, biografia, fecha_nacimiento, fecha_muerte, ruta_img):
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.biografia = biografia
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_muerte = fecha_muerte
        self.ruta_img = ruta_img

    def __repr__(self):
        return "<Producto (identificacion = ' % s ', nombres = ' % s ', apellidos = ' % s ', biografia = ' % s ', fecha_nacimiento = ' % s ', fecha_muerte = ' % s', rutaImg = ' % s')>" % (
            self.identificacion, self.nombres, self.apellidos, self.biografia, self.fecha_nacimiento, self.fecha_muerte, self.ruta_img)


class Libro(Base):
    __tablename__ = 'libro'
    ISBN = Column(String(20), primary_key=True)
    titulo = Column(String(80))
    fecha_publicacion = Column(Date)
    idioma_original = Column(String(10))
    resumen = Column(String)
    id_autor = Column(Integer, ForeignKey("autor.identificacion"))
    parent = relationship("Autor", backref=backref("libro", uselist=False))

    def __init__(self, ISBN, titulo, fecha_publicacion, idioma_original, resumen, id_autor):
        self.ISBN = ISBN
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.idioma_original = idioma_original
        self.resumen = resumen
        self.id_autor = id_autor

    def __repr__(self):
        return "<Carrito (ISBN = ' % s  ', titulo = ' % s ', fecha_publicacion = ' % s ', idioma_original = ' % s', resumen = ' % s', id_autor = ' % s')>" % (
            self.ISBN, self.titulo, self.fecha_publicacion, self.idioma_original, self.resumen, self.id_autor)

association_table  = Table(
    'association',
    Base.metadata,
    Column("id_articulo",Integer, ForeignKey("articulo.ISSN"), primary_key=True),
    Column("id_autor", String, ForeignKey("autor.identificacion"), primary_key=True)
)

class Articulo(Base):
    __tablename__ = 'articulo'
    issn = Column(Integer, primary_key=True)
    paginas = Column(Integer)
    titulo = Column(String(100))
    fecha_publicacion = Column(Date)
    publicacion = Column(String(200))
    resumen = Column(String)
    autor = relationship(
        "Autor", secondary=association_table, backref="libros"
    )

    def __init__(self, titulo, issn, paginas, fecha_publicacion, publicacion, resumen):
        self.issn = issn
        self.paginas = paginas
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.publicacion = publicacion
        self.resumen = resumen

    def __repr__(self):
        return "<producto_carrito (ISSN = ' % s ', paginas = ' % s ', titulo = ' % s ', cantidad = ' % s', resumen = ' % s')>" % (
            self.issn, self.paginas, self.titulo, self.publicacion, self.resumen)




if __name__ == '__main__':
    motor = 'postgresql'
    database = 'biblioteca'
    puerto = '5432'
    usuario = 'postgres'
    contrasenia = 'root'
    host = 'localhost'

    engine = create_engine(
        motor + '://' + usuario + ':' + contrasenia + '@' + host + ':' + puerto + '/' + database)
    Base.metadata.create_all(engine)
