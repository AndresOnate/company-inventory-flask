from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db

class RoleEnum(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    roles = db.Column(db.String(50), nullable=False)  # Solo como texto para simplificar

    def __init__(self, name, email, password, roles=None):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)  # Contraseña segura
        self.roles = 'ADMIN' if roles is None else ','.join(roles)
    
    def __repr__(self):
        return f'<User {self.name}>'

    @classmethod
    def create_user(cls, name, email, password, roles=None):
        user = cls(name=name, email=email, password=password, roles=roles)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def update_user(self, name=None, email=None, password=None, roles=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = generate_password_hash(password)
        if roles:
            self.roles = ','.join(roles)
        db.session.commit()
        return self

    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_roles(self):
        return self.roles.split(',')  # Convierte el string de roles a una lista

    def has_role(self, role):
        return role in self.get_roles()
