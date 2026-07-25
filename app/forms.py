from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, validators, IntegerField
from utils.analysis_utils import validar_correo
import re



def mailValidation(form, campo):
    correovalidation = validar_correo(campo.data)
    if correovalidation == False:
        raise ValidationError('El dominio no corresponde a wolfsellers.com o adobe.com')

def codigoValidation(form, campo):
    if len(str(campo)) < 4:
        raise ValidationError ('El código no debe ser menor a 4 dígitos')
    elif len(str(campo)) > 4:
        raise ValidationError('El codigo no debe de ser mayor a 4 dígitos')


class FormLogin(FlaskForm):
    correo = StringField('Correo electrónico', validators=[mailValidation])
    contraseña = PasswordField('Contraseña')
    submit = SubmitField('Iniciar Sesión')

class FormRegistro(FlaskForm):
    correo = StringField('Correo electrónico', validators=[mailValidation])
    contraseña = PasswordField('Contraseña', validators=[validators.DataRequired(), validators.EqualTo('confirm_contraseña', message='Las contraseñas deben coincidir')])
    confirm_contraseña = PasswordField('Confirmar Contraseña')
    submit = SubmitField('Enviar')


class FormVerfificacion(FlaskForm):
    codigo = IntegerField('Código de Verificación', validators=[codigoValidation])
    submit = SubmitField('Enviar')


class FormUrl(FlaskForm):
    url = StringField('URL de la página')
    submit = SubmitField('ANALIZAR')