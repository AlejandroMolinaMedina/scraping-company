import os

# Comentario para activar GitHub Action
# Clase config para hacer la conexión con la BD
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    POSTGRES_USER = os.environ.get('DB_USER')
    POSTGRES_PASSWORD = os.environ.get('DB_PASSWORD')
    POSTGRES_HOST = os.environ.get('DB_HOST')
    POSTGRES_DB = os.environ.get('DB_NAME') 
    

    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD') 
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_USE_SSL = False
    SESSION_TYPE = 'filesystem'