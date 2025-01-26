from flask_sqlalchemy import SQLAlchemy
from app import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relación Many-to-Many con productos
    products = db.relationship('Product', secondary='product_category', back_populates='categories')

    def __repr__(self):
        return f'<Category {self.name}>'

    @classmethod
    def create_category(cls, name):
        category = cls(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_category_by_id(cls, category_id):
        return cls.query.get(category_id)

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()

    def update_category(self, name=None):
        if name:
            self.name = name
        db.session.commit()
        return self

    @classmethod
    def delete_category(cls, category_id):
        category = cls.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False
