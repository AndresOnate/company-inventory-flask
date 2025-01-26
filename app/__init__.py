from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

# Base class for models
class Base(DeclarativeBase):
    pass

# Initialize the database and migration instances
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        app: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)  # Configurations loaded from config.py
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for specific routes

    # Initialize the extensions
    db.init_app(app)  # Set up the database
    migrate.init_app(app, db)  # Set up migration

    # Importing models for use in the app
    from app.users.models import User
    from app.category.models import Category
    from app.client.models import Client
    from app.company.models import Company
    from app.product.models import Product
    from app.order.models import Order

    # Importing controllers (blueprints) for routing
    from app.users.user_controller import user_bp
    from app.auth.auth_controller import auth_bp
    from app.company.company_controller import company_bp
    from app.category.category_controller import category_bp
    from app.client.client_controller import client_bp
    from app.product.product_controller import product_bp
    from app.email.email_controller import email_bp
    
    # Registering the blueprints with the app
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(client_bp) 
    app.register_blueprint(product_bp)
    app.register_blueprint(email_bp)

    # Create all the tables defined by models
    with app.app_context(): 
        db.create_all()

    return app
