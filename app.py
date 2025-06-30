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
        
        # Agregar filtro personalizado para fechas en zona horaria de Perú
        from datetime import datetime, timezone, timedelta
        
        @app.template_filter('peru_datetime')
        def peru_datetime_filter(dt_string):
            """Convierte timestamp ISO a formato legible en zona horaria de Perú"""
            try:
                # Si es string ISO, convertir a datetime
                if isinstance(dt_string, str):
                    # Parsear timestamp ISO
                    if dt_string.endswith('Z'):
                        dt = datetime.fromisoformat(dt_string[:-1] + '+00:00')
                    elif '+' in dt_string or dt_string.count('-') > 2:
                        dt = datetime.fromisoformat(dt_string)
                    else:
                        dt = datetime.fromisoformat(dt_string)
                        # Asumir UTC si no hay timezone
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt_string
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                
                # Convertir a zona horaria de Perú
                peru_tz = timezone(timedelta(hours=-5))
                dt_peru = dt.astimezone(peru_tz)
                
                # Formatear en español
                months = [
                    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
                ]
                
                day = dt_peru.day
                month = months[dt_peru.month - 1]
                year = dt_peru.year
                time = dt_peru.strftime('%H:%M:%S')
                
                return f"{day} de {month} de {year} a las {time} (Perú)"
                
            except Exception as e:
                return str(dt_string)  # Fallback al string original
        
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
