from app import db
from datetime import datetime
import json
import pytz

PERU_TZ = pytz.timezone('America/Lima')

class Election(db.Model):
    """Administrar elecciones"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    options = db.Column(db.Text, nullable=False)  # JSON string para opciones de votación
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(PERU_TZ).replace(tzinfo=None))

    def get_options(self):
        """Convierte el JSON almacenado en una lista de Python"""
        return json.loads(self.options)

    def set_options(self, options_list):
        """Convierte una lista Python a JSON para almacenar en la BD"""
        """Cuando el admin crea una nueva elección, se convierte la lista de opciones en un JSON"""
        self.options = json.dumps(options_list)

class VerificationCode(db.Model):
    """Conecta códigos de verificación con elecciones específicas"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    election = db.relationship('Election', backref='verification_codes')

class VoterHistory(db.Model):
    """Garantiza que un email solo vote UNA vez por elección"""
    id = db.Column(db.Integer, primary_key=True)
    email_hash = db.Column(db.String(64), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=lambda: datetime.now(PERU_TZ).replace(tzinfo=None))

    election = db.relationship('Election', backref='voter_history')

    __table_args__ = (db.UniqueConstraint('email_hash', 'election_id', name='unique_voter_election'),)