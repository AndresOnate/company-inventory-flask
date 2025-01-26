from flask_sqlalchemy import SQLAlchemy
from app import db

product_category = db.Table(
    'product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Relación Many-to-One con compañía
    company_nit = db.Column(db.String(50), db.ForeignKey('companies.nit'))
    company = db.relationship('Company', back_populates='products')

    # Relación Many-to-Many con órdenes
    orders = db.relationship('Order', secondary=order_product, back_populates='products')

    # Relación Many-to-Many con categorías
    categories = db.relationship('Category', secondary=product_category, back_populates='products')

    def __repr__(self):
        return f'<Product {self.name}>'

    @classmethod
    def create_product(cls, code, name, description, price, quantity, company_nit):
        product = cls(code=code, name=name, description=description, price=price, quantity=quantity, company_nit=company_nit)
        db.session.add(product)
        db.session.commit()
        return product

    @classmethod
    def get_product_by_id(cls, product_id):
        return cls.query.get(product_id)

    @classmethod
    def get_all_products(cls):
        return cls.query.all()

    def update_product(self, code =None, name=None, description=None, price=None, quantity=None, company_nit=None):
        if code:
            self.code = code
        if name:
            self.name = name
        if description:
            self.description = description
        if price:
            self.price = price
        if quantity:
            self.quantity = quantity
        if company_nit:
            self.company_nit = company_nit
        db.session.commit()
        return self

    @classmethod
    def delete_product(cls, product_id):
        product = cls.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
