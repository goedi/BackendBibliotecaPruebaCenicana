
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean
from sqlalchemy.orm import backref, relationship
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
    estado = Column(Boolean, default=True)

    def __init__(self, identificacion, nombres,  apellidos, biografia, fecha_nacimiento, fecha_muerte, ruta_img, estado):
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.biografia = biografia
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_muerte = fecha_muerte
        self.ruta_img = ruta_img
        self.estado = estado

    def __repr__(self):
        return "<Producto (identificacion = ' % s ', nombres = ' % s ', apellidos = ' % s ', biografia = ' % s ', fecha_nacimiento = ' % s ', fecha_muerte = ' % s', rutaImg = ' % s', estado = ' % s')>" % (
            self.identificacion, self.nombres, self.apellidos, self.biografia, self.fecha_nacimiento, self.fecha_muerte, self.ruta_img, self.estado)


class Libro(Base):
    __tablename__ = 'libro'
    ISBN = Column(String(20), primary_key=True)
    titulo = Column(String(80))
    fecha_publicacion = Column(Date)
    idioma_original = Column(String(10))
    resumen = Column(String)
    id_autor = Column(String, ForeignKey("autor.identificacion"))
    estado = Column(Boolean, default=True)
    parent = relationship("Autor", backref=backref("libro", uselist=False))

    def __init__(self, ISBN, titulo, fecha_publicacion, idioma_original, resumen, id_autor, estado):
        self.ISBN = ISBN
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.idioma_original = idioma_original
        self.resumen = resumen
        self.id_autor = id_autor
        self.estado = estado

    def __repr__(self):
        return "<Carrito (ISBN = ' % s  ', titulo = ' % s ', fecha_publicacion = ' % s ', idioma_original = ' % s', resumen = ' % s', id_autor = ' % s', estado = ' % s')>" % (
            self.ISBN, self.titulo, self.fecha_publicacion, self.idioma_original, self.resumen, self.id_autor, self.estado)


association_table = Table(
    'association',
    Base.metadata,
    Column("id_articulo", Integer, ForeignKey(
        "articulo.issn"), primary_key=True),
    Column("id_autor", String, ForeignKey(
        "autor.identificacion"), primary_key=True)
)


class AutorArticulo(Base):
    __tablename__ = 'autor_articulo'
    id_articulo = Column(Integer, ForeignKey(
        "articulo.issn"), primary_key=True)
    id_autor = Column(String, ForeignKey(
        "autor.identificacion"), primary_key=True)

    def __init__(self, id_articulo, id_autor):
        self.id_articulo = id_articulo
        self.id_autor = id_autor


class Articulo(Base):
    __tablename__ = 'articulo'
    issn = Column(Integer, primary_key=True)
    paginas = Column(Integer)
    titulo = Column(String(100))
    fecha_publicacion = Column(Date)
    publicacion = Column(String(200))
    resumen = Column(String)
    estado = Column(Boolean, default=True)
    autor = relationship(
        "Autor", secondary='autor_articulo', backref="articulos"
    )

    def __init__(self, titulo, issn, paginas, fecha_publicacion, publicacion, resumen, estado):
        self.issn = issn
        self.paginas = paginas
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.publicacion = publicacion
        self.resumen = resumen
        self.estado = estado

    def __repr__(self):
        return "<producto_carrito (ISSN = ' % s ', paginas = ' % s ', titulo = ' % s ', cantidad = ' % s', resumen = ' % s', estado = ' % s')>" % (
            self.issn, self.paginas, self.titulo, self.publicacion, self.resumen, self.estado)


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
