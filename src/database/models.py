from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Date
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    fullname = Column(String(30), nullable=False)
    email = Column(String(40), nullable=False)
    phone_number = Column(String(13), nullable=False)
    birthday = Column(Date, nullable=False)
    description = Column(String(150))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), nullable=True, onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", backref='todos', lazy='joined')


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(250), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    confirmed = Column(Boolean, default=False, nullable=True)
