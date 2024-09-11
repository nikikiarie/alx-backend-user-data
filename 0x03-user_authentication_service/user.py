#!/usr/bin/env python3
"""
User module
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    User table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(20), nullable=False)
    hash_password = Column(String(20), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

