from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(40), nullable=False)
    content = Column(String(200), nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)