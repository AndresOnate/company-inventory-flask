from flask_sqlalchemy import SQLAlchemy
from app import db

class Company(db.Model):
    """
    Model representing a company in the database.
    The class handles CRUD operations (create, read, update, delete) and
    establishes a One-to-Many relationship with the Product entity.
    """
    __tablename__ = 'companies'
    nit = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    # One-to-Many relationship with products
    products = db.relationship('Product', back_populates='company', cascade='all, delete')

    def __repr__(self):
        """
        String representation of the company. Displays the company name.
        """
        return f'<Company {self.name}>'

    @classmethod
    def create_company(cls, nit, name, address=None, phone=None):
        """
        Creates a new company in the database.
        
        Args:
            nit (str): The company's tax identification number (NIT).
            name (str): The company's name.
            address (str, optional): The company's address.
            phone (str, optional): The company's phone number.
        
        Returns:
            Company: The newly created company.
        """
        company = cls(nit=nit, name=name, address=address, phone=phone)
        db.session.add(company)
        db.session.commit()
        return company

    @classmethod
    def get_company_by_nit(cls, nit):
        """
        Retrieves a company by its NIT (Tax Identification Number).
        
        Args:
            nit (str): The NIT of the company to search for.
        
        Returns:
            Company: The found company, or None if it doesn't exist.
        """
        return cls.query.get(nit)

    @classmethod
    def get_all_companies(cls):
        """
        Retrieves all companies registered in the database.
        
        Returns:
            list: A list of all companies.
        """
        return cls.query.all()

    def update_company(self, name=None, address=None, phone=None):
        """
        Updates a company's data in the database.
        
        Args:
            name (str, optional): The new name for the company.
            address (str, optional): The new address for the company.
            phone (str, optional): The new phone number for the company.
        
        Returns:
            Company: The updated company.
        """
        if name:
            self.name = name
        if address:
            self.address = address
        if phone:
            self.phone = phone
        db.session.commit()
        return self

    @classmethod
    def delete_company(cls, nit):
        """
        Deletes a company from the database using its NIT.
        
        Args:
            nit (str): The NIT of the company to delete.
        
        Returns:
            bool: True if the company was successfully deleted, False if the company was not found.
        """
        company = cls.query.get(nit)
        if company:
            db.session.delete(company)
            db.session.commit()
            return True
        return False
