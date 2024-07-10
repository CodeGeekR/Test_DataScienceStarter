from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialización de extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        # Importación de modelos y blueprints
        from app.models import Usuario
        from app.views import bp as main_blueprint

        app.register_blueprint(main_blueprint)

        # Cargador de usuario para flask_login
        @login_manager.user_loader
        def load_user(user_id):
            return Usuario.query.get(int(user_id))
        
        # Verificación y creación de tablas en la base de datos
        # Si las tablas no existen, se crean según los modelos definidos
        # db.create_all()

    return app