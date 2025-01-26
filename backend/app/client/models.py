from flask_sqlalchemy import SQLAlchemy
from app import db

class Client(db.Model):
    """
    The `Client` class represents a client in the database. It contains fields 
    for the client's personal information, such as `name` and `email`, and has 
    methods for creating, retrieving, updating, and deleting clients. Additionally, 
    it defines a one-to-many relationship with the `Order` model, meaning that 
    each client can have multiple associated orders.
    """
    
    __tablename__ = 'clients'
    
    # Database Columns
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the client
    name = db.Column(db.String(100), nullable=False)  # Name of the client
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email of the client (must be unique)

    # Relationship: A client can have many orders
    orders = db.relationship('Order', back_populates='client', cascade='all, delete')

    def __repr__(self):
        """
        Returns a string representation of the Client object for easy display 
        and debugging.

        Returns:
            str: A string in the format <Client name>, e.g., <Client John Doe>
        """
        return f'<Client {self.name}>'

    @classmethod
    def create_client(cls, name, email):
        """
        Creates a new client and adds it to the database.

        Args:
            name (str): The name of the client.
            email (str): The email of the client (must be unique).

        Returns:
            Client: The created Client object.
        """
        # Create a new client
        client = cls(name=name, email=email)
        
        # Add and commit the new client to the database
        db.session.add(client)
        db.session.commit()
        
        return client

    @classmethod
    def get_client_by_id(cls, client_id):
        """
        Retrieves a client by their unique identifier (ID).

        Args:
            client_id (int): The unique identifier of the client.

        Returns:
            Client: The client object if found, or None if no client exists with the given ID.
        """
        return cls.query.get(client_id)

    @classmethod
    def get_all_clients(cls):
        """
        Retrieves all clients from the database.

        Returns:
            list: A list of all Client objects.
        """
        return cls.query.all()

    def update_client(self, name=None, email=None):
        """
        Updates the client's information.

        Args:
            name (str, optional): The new name of the client.
            email (str, optional): The new email of the client.

        Returns:
            Client: The updated Client object.
        """
        if name:
            self.name = name
        if email:
            self.email = email
        
        # Commit changes to the database
        db.session.commit()
        
        return self

    @classmethod
    def delete_client(cls, client_id):
        """
        Deletes a client from the database by their unique identifier (ID).

        Args:
            client_id (int): The unique identifier of the client to delete.

        Returns:
            bool: True if the client was successfully deleted, False if no client 
                  exists with the provided ID.
        """
        # Retrieve the client by ID
        client = cls.query.get(client_id)
        
        # If the client exists, delete them and commit the transaction
        if client:
            db.session.delete(client)
            db.session.commit()
            return True
        
        return False
