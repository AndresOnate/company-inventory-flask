from flask_sqlalchemy import SQLAlchemy
from app import db


class Order(db.Model):
    """
    Represents an order in the database, managing CRUD operations (create, read, update, delete).
    The class establishes a Many-to-One relationship with the Client entity and a Many-to-Many relationship with the Product entity.
    
    Attributes:
        id (int): The primary key, unique identifier for the order.
        order_date (str): The date the order was placed.
        client_id (int): The foreign key referencing the client associated with the order.
        client (Client): The client associated with the order.
        products (list): A list of products associated with the order.
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.String(50), nullable=False)

    # Many-to-One relationship with client
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='orders')

    # Many-to-Many relationship with products
    products = db.relationship('Product', secondary='order_product', back_populates='orders')

    def __repr__(self):
        """
        String representation of the order, displaying the order's ID.
        """
        return f'<Order {self.id}>'

    @classmethod
    def create_order(cls, order_date, client_id):
        """
        Creates a new order in the database.
        
        Args:
            order_date (str): The date the order was placed.
            client_id (int): The ID of the client placing the order.
        
        Returns:
            Order: The newly created order.
        """
        order = cls(order_date=order_date, client_id=client_id)
        db.session.add(order)
        db.session.commit()
        return order

    @classmethod
    def get_order_by_id(cls, order_id):
        """
        Fetches an order by its ID.
        
        Args:
            order_id (int): The ID of the order to retrieve.
        
        Returns:
            Order: The order object if found, or None if not.
        """
        return cls.query.get(order_id)

    @classmethod
    def get_all_orders(cls):
        """
        Fetches all orders from the database.
        
        Returns:
            list: A list of all orders.
        """
        return cls.query.all()

    def update_order(self, order_date=None, client_id=None):
        """
        Updates the details of an existing order.
        
        Args:
            order_date (str, optional): The new order date.
            client_id (int, optional): The new client ID associated with the order.
        
        Returns:
            Order: The updated order.
        """
        if order_date:
            self.order_date = order_date
        if client_id:
            self.client_id = client_id
        db.session.commit()
        return self

    @classmethod
    def delete_order(cls, order_id):
        """
        Deletes an order from the database using its ID.
        
        Args:
            order_id (int): The ID of the order to delete.
        
        Returns:
            bool: True if the order was deleted successfully, False if not found.
        """
        order = cls.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False
