from flask_sqlalchemy import SQLAlchemy
from app import db

class Category(db.Model):
    """
    The Category model represents a product category.

    Attributes:
        id (int): The primary key for the category.
        name (str): The name of the category.
        products (relationship): A many-to-many relationship with the Product model.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Many-to-many relationship with products
    products = db.relationship('Product', secondary='product_category', back_populates='categories')

    def __repr__(self):
        """
        Return a string representation of the Category object.
        """
        return f'<Category {self.name}>'

    @classmethod
    def create_category(cls, name):
        """
        Create a new category and save it to the database.

        Args:
            name (str): The name of the new category.

        Returns:
            Category: The newly created category object.
        """
        category = cls(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_category_by_id(cls, category_id):
        """
        Retrieve a category by its ID.

        Args:
            category_id (int): The ID of the category to retrieve.

        Returns:
            Category or None: The category with the specified ID, or None if not found.
        """
        return cls.query.get(category_id)

    @classmethod
    def get_all_categories(cls):
        """
        Retrieve all categories from the database.

        Returns:
            list[Category]: A list of all categories in the database.
        """
        return cls.query.all()

    def update_category(self, name=None):
        """
        Update the category's attributes.

        Args:
            name (str, optional): The new name for the category. Defaults to None.

        Returns:
            Category: The updated category object.
        """
        if name:
            self.name = name
        db.session.commit()
        return self

    @classmethod
    def delete_category(cls, category_id):
        """
        Delete a category by its ID.

        Args:
            category_id (int): The ID of the category to delete.

        Returns:
            bool: True if the category was deleted, False if not found.
        """
        category = cls.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False
