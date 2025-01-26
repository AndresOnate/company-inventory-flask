from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db

# Enum for user roles
class RoleEnum(Enum):
    """
    Enum class to define different user roles.

    Roles:
        - ADMIN: Admin user
        - USER: Regular user
    """
    ADMIN = 'ADMIN'
    USER = 'USER'

# User model class for handling user data in the database
class User(db.Model):
    """
    User model representing the 'users' table in the database.
    
    Attributes:
        - id (int): Unique identifier for the user (primary key).
        - name (str): Name of the user.
        - email (str): User's email address (unique).
        - password (str): User's password (hashed).
        - roles (str): A comma-separated string of roles assigned to the user.
    """
    __tablename__ = 'users'

    # Define the columns in the 'users' table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    roles = db.Column(db.String(50), nullable=False)  # Stored as a comma-separated string for simplicity

    def __init__(self, name, email, password, roles=None):
        """
        Initializes a new User object.
        
        Args:
            name (str): User's name.
            email (str): User's email.
            password (str): User's password (plain text).
            roles (list): List of roles to assign to the user (optional, default is 'ADMIN').
        """
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)  # Store a hashed password
        self.roles = 'ADMIN' if roles is None else ','.join(roles)  # Default role is ADMIN if none is provided
    
    def __repr__(self):
        """
        String representation of the User object.
        
        Returns:
            (str): A string representing the user.
        """
        return f'<User {self.name}>'

    # Class methods to interact with the database

    @classmethod
    def create_user(cls, name, email, password, roles=None):
        """
        Creates a new user and adds it to the database.

        Args:
            name (str): User's name.
            email (str): User's email.
            password (str): User's password (plain text).
            roles (list): List of roles to assign to the user (optional).

        Returns:
            (User): The created user object.
        """
        user = cls(name=name, email=email, password=password, roles=roles)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_user_by_id(cls, user_id):
        """
        Retrieves a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            (User): The user object if found, else None.
        """
        return cls.query.get(user_id)

    @classmethod
    def get_all_users(cls):
        """
        Retrieves all users from the database.

        Returns:
            (list): A list of all user objects.
        """
        return cls.query.all()
    
    @classmethod
    def get_user_by_email(cls, email):
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            (User): The user object if found, else None.
        """
        return cls.query.filter_by(email=email).first()

    def update_user(self, name=None, email=None, password=None, roles=None):
        """
        Updates the user's details.

        Args:
            name (str, optional): New name for the user.
            email (str, optional): New email for the user.
            password (str, optional): New password for the user (plain text).
            roles (list, optional): New roles for the user.
        
        Returns:
            (User): The updated user object.
        """
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
        """
        Deletes a user from the database by their ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            (bool): True if the user was deleted, False if not found.
        """
        user = cls.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.

        Args:
            password (str): The plain text password to check.

        Returns:
            (bool): True if the passwords match, False otherwise.
        """
        return check_password_hash(self.password, password)
    
    def get_roles(self):
        """
        Retrieves the list of roles assigned to the user.

        Returns:
            (list): A list of roles.
        """
        return self.roles.split(',')  # Converts the roles string into a list

    def has_role(self, role):
        """
        Checks if the user has a specific role.

        Args:
            role (str): The role to check for.

        Returns:
            (bool): True if the user has the role, False otherwise.
        """
        return role in self.get_roles()
