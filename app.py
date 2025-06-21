import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Configura logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Crea la app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "voting-blockchain-secret-key")

# Configura la base de datos - usar SQLite por defecto para estabilidad
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voting.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

# Inicializa la base de datos
db.init_app(app)

def initialize_app():
    """Inicializa la aplicación con manejo de errores"""
    try:
        with app.app_context():
            # Importa modelos para crear tablas
            import models
            db.create_all()
            
        # Importa rutas después de inicializar la app
        import routes
        
        # Inicializa blockchain y email service
        from blockchain import voting_blockchain
        from email_service import email_service
        
        logging.info("Aplicación inicializada correctamente")
        return True
        
    except Exception as e:
        logging.error(f"Error inicializando la aplicación: {e}")
        # Si falla PostgreSQL, intenta SQLite
        if "postgresql" in str(e).lower():
            logging.info("Cambiando a SQLite...")
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voting.db"
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
            db.init_app(app)
            try:
                with app.app_context():
                    import models
                    db.create_all()
                logging.info("SQLite inicializado correctamente")
                return True
            except Exception as sqlite_error:
                logging.error(f"Error con SQLite: {sqlite_error}")
                return False
        return False

# Inicializa la aplicación
if not initialize_app():
    logging.error("No se pudo inicializar la aplicación")
    exit(1)
