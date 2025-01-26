from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    # Inicializa las extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    from app.users.models import User
    from app.category.models import Category
    from app.client.models import Client
    from app.company.models import Company
    from app.product.models import Product
    from app.order.models import Order

    from app.users.user_controller import user_bp
    from app.auth.auth_controller import auth_bp
    from app.company.company_controller import company_bp
    from app.category.category_controller import category_bp
    from app.client.client_controller import client_bp
    from app.product.product_controller import product_bp
    from app.email.email_controller import email_bp
    
    
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(client_bp) 
    app.register_blueprint(product_bp)
    app.register_blueprint(email_bp)
    with app.app_context():  # Asegúrate de que el contexto esté disponible
        db.create_all() 

    return app
