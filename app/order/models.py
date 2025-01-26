from flask_sqlalchemy import SQLAlchemy
from app import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.String(50), nullable=False)

    # Relación Many-to-One con cliente
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='orders')

    # Relación Many-to-Many con productos
    products = db.relationship('Product', secondary='order_product', back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}>'

    @classmethod
    def create_order(cls, order_date, client_id):
        order = cls(order_date=order_date, client_id=client_id)
        db.session.add(order)
        db.session.commit()
        return order

    @classmethod
    def get_order_by_id(cls, order_id):
        return cls.query.get(order_id)

    @classmethod
    def get_all_orders(cls):
        return cls.query.all()

    def update_order(self, order_date=None, client_id=None):
        if order_date:
            self.order_date = order_date
        if client_id:
            self.client_id = client_id
        db.session.commit()
        return self

    @classmethod
    def delete_order(cls, order_id):
        order = cls.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False
