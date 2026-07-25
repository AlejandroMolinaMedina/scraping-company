from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
from flask_login import LoginManager
from datetime import datetime, timedelta


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate = Migrate(app, db)


    app.permanent_session_lifetime = timedelta(seconds=1800)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'  # La ruta a la página de inicio de sesión

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario  # Ajusta la importación según la estructura de tu proyecto
        return db.session.query(Usuario).get(int(user_id))

    from app import routes  # Importa tus rutas después de configurar todo

    return app
