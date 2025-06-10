from app import db
from datetime import datetime
import json

class Election(db.Model):
    """Model for managing elections"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    options = db.Column(db.Text, nullable=False)  # JSON string of voting options
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_options(self):
        """Get voting options as a list"""
        return json.loads(self.options)
    
    def set_options(self, options_list):
        """Set voting options from a list"""
        self.options = json.dumps(options_list)

class VerificationCode(db.Model):
    """Model for email verification codes"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    election = db.relationship('Election', backref='verification_codes')

class VoterHistory(db.Model):
    """Model to track if a voter has already voted (without storing the vote itself)"""
    id = db.Column(db.Integer, primary_key=True)
    email_hash = db.Column(db.String(64), nullable=False)  # Hashed email for privacy
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    election = db.relationship('Election', backref='voter_history')
    
    __table_args__ = (db.UniqueConstraint('email_hash', 'election_id', name='unique_voter_election'),)
