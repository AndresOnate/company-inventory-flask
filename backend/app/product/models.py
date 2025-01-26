from flask_sqlalchemy import SQLAlchemy
from app import db

# Association table for the many-to-many relationship between products and categories
product_category = db.Table(
    'product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

# Association table for the many-to-many relationship between orders and products
order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

class Product(db.Model):
    """
    Represents a product in the database, including its attributes and relationships with other entities.

    Attributes:
        id (int): The unique identifier for the product (Primary key).
        code (str): The unique code assigned to the product.
        name (str): The name of the product.
        description (str): A textual description of the product.
        price (float): The price of the product.
        quantity (int): The available quantity of the product in stock.
        company_nit (str): The tax identification number (NIT) of the company associated with the product.
        company (Company): The company related to the product (Many-to-One relationship).
        orders (list): The list of orders associated with the product (Many-to-Many relationship).
        categories (list): The list of categories to which the product belongs (Many-to-Many relationship).
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Many-to-One relationship with Company (a product is associated with one company)
    company_nit = db.Column(db.String(50), db.ForeignKey('companies.nit'))
    company = db.relationship('Company', back_populates='products')

    # Many-to-Many relationship with Orders (a product can be part of many orders)
    orders = db.relationship('Order', secondary=order_product, back_populates='products')

    # Many-to-Many relationship with Categories (a product can belong to many categories)
    categories = db.relationship('Category', secondary=product_category, back_populates='products')

    def __repr__(self):
        """
        Provides a string representation of the product object, displaying its name.
        
        Returns:
            str: A string representation of the product's name.
        """
        return f'<Product {self.name}>'

    @classmethod
    def create_product(cls, code, name, description, price, quantity, company_nit):
        """
        Creates and saves a new product to the database.
        
        Args:
            code (str): The unique product code.
            name (str): The product's name.
            description (str): A description of the product.
            price (float): The price of the product.
            quantity (int): The available quantity of the product.
            company_nit (str): The NIT of the company associated with the product.
        
        Returns:
            Product: The newly created product instance.
        """
        product = cls(code=code, name=name, description=description, price=price, quantity=quantity, company_nit=company_nit)
        db.session.add(product)
        db.session.commit()
        return product

    @classmethod
    def get_product_by_id(cls, product_id):
        """
        Fetches a product from the database by its ID.
        
        Args:
            product_id (int): The ID of the product to retrieve.
        
        Returns:
            Product: The product instance if found, otherwise None.
        """
        return cls.query.get(product_id)

    @classmethod
    def get_all_products(cls):
        """
        Retrieves all products from the database.
        
        Returns:
            list: A list of all product instances.
        """
        return cls.query.all()

    def update_product(self, code=None, name=None, description=None, price=None, quantity=None, company_nit=None):
        """
        Updates the attributes of an existing product in the database.
        
        Args:
            code (str, optional): The new product code.
            name (str, optional): The new product name.
            description (str, optional): The new product description.
            price (float, optional): The new product price.
            quantity (int, optional): The new product quantity.
            company_nit (str, optional): The new company NIT.
        
        Returns:
            Product: The updated product instance.
        """
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
        """
        Deletes a product from the database by its ID.
        
        Args:
            product_id (int): The ID of the product to delete.
        
        Returns:
            bool: True if the product was deleted successfully, False if the product was not found.
        """
        product = cls.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
