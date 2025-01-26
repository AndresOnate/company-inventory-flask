from flask_sqlalchemy import SQLAlchemy
from app import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relación One-to-Many con órdenes
    orders = db.relationship('Order', back_populates='client', cascade='all, delete')

    def __repr__(self):
        return f'<Client {self.name}>'

    @classmethod
    def create_client(cls, name, email):
        client = cls(name=name, email=email)
        db.session.add(client)
        db.session.commit()
        return client

    @classmethod
    def get_client_by_id(cls, client_id):
        return cls.query.get(client_id)

    @classmethod
    def get_all_clients(cls):
        return cls.query.all()

    def update_client(self, name=None, email=None):
        if name:
            self.name = name
        if email:
            self.email = email
        db.session.commit()
        return self

    @classmethod
    def delete_client(cls, client_id):
        client = cls.query.get(client_id)
        if client:
            db.session.delete(client)
            db.session.commit()
            return True
        return False
