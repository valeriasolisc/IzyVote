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

# Configura la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///instance/voting.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Inicializa la base de datos
db.init_app(app)

with app.app_context():
    # Importa modelos para crear tablas
    import models
    db.create_all()

# Importa rutas después de inicializar la app
import routes
