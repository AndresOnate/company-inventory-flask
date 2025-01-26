from flask_sqlalchemy import SQLAlchemy
from app import db

class Company(db.Model):
    __tablename__ = 'companies'
    nit = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    # Relación One-to-Many con productos
    products = db.relationship('Product', back_populates='company', cascade='all, delete')

    def __repr__(self):
        return f'<Company {self.name}>'

    @classmethod
    def create_company(cls, nit, name, address=None, phone=None):
        company = cls(nit=nit, name=name, address=address, phone=phone)
        db.session.add(company)
        db.session.commit()
        return company

    @classmethod
    def get_company_by_nit(cls, nit):
        return cls.query.get(nit)

    @classmethod
    def get_all_companies(cls):
        return cls.query.all()

    def update_company(self, name=None, address=None, phone=None):
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
        company = cls.query.get(nit)
        if company:
            db.session.delete(company)
            db.session.commit()
            return True
        return False
