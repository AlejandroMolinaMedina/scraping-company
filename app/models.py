from app import db
from flask_login import UserMixin





class TipoUsuario(db.Model):
    __tablename__ = 'tipousuario'
    id_TipoUsuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20))

    def _repr_(self):
        return f"TipoUsuario('{self.descripcion}')"


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id_Usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    codigoSecreto = db.Column(db.String(170), nullable=False)
    contrasenia = db.Column(db.String(170), nullable= False)
    tipoUsuario = db.Column(db.Integer, nullable = False)

    id_tipoUsuario = db.Column(db.Integer, db.ForeignKey('tipousuario.id_TipoUsuario'))

    tipoUsuario = db.relationship(TipoUsuario, backref='tipoUsuario', lazy=True)
    def is_active(self):
        return True  # Puedes personalizar esta lógica según tus necesidades

    def get_id(self):
        return str(self.id_Usuario)  # Convierte el ID a cadena, ya que Flask-Login espera una cadena




class Informe(db.Model):
    id_Informe = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(14), nullable=False)
    json_name = db.Column(db.String(100), nullable=False)
    pdf_name = db.Column(db.String(100), nullable=False)

    def _repr_(self):
        return f"Informe('{self.nombre}','{self.url}')"

class Comentario(db.Model):  # Corregir el nombre de la clase
    id_Comentario = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)

    id_informe = db.Column(db.Integer, db.ForeignKey('informe.id_Informe'))  # Corregir el nombre de la tabla

    informe = db.relationship(Informe, backref='comentarios', lazy=True)