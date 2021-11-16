"""from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime
import enum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    #receipts = relationship("ReceiptDetail", backref="product", lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now())
    details = relationship("ReceiptDetail", backref="receipt", lazy=True)

    def __str__(self):
        return str(self.id)


class ReceiptDetail(BaseModel):
    product_id = Column(Integer, ForeignKey(Product.id))
    receipt_id = Column(Integer, ForeignKey(Receipt.id))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)



if __name__ == '__main__':
    db.create_all()
"""