from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.database import db

from .session import Session


# from app.database import db

class User(db.Model,UserMixin):  # We'll bind it to db.Model later
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'staff', or 'student'
    
    # Relationships
    sessions = db.relationship('Session', backref='user', lazy=True)
    materials = db.Column(db.String, nullable=True)  # Only relevant for students but can be null for others

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

