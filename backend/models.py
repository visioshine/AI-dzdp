from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
    avatar = Column(String, nullable=True)
    bio = Column(Text, nullable=True)  # 个人简介
    catchphrase = Column(String, nullable=True)  # 口头禅
    gender = Column(String, nullable=True)  # 性别
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="author")

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    address = Column(String)
    category = Column(String, index=True)
    phone = Column(String)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="merchant")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="reviews")
    merchant = relationship("Merchant", back_populates="reviews")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="favorites")
    merchant = relationship("Merchant", backref="favorites")

class PasswordResetEmail(Base):
    __tablename__ = "password_reset_emails"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    verification_code = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_used = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="password_reset_emails")
