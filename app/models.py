from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)  # Specify length

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Specify length
    email = Column(String(255), unique=True, index=True)  # Specify length
    password = Column(String(255))  # Specify length
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Specify length
    description = Column(String(255))  # Specify length
    price = Column(Float)
    image_url = Column(String(255))  # Specify length