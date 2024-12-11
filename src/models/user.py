from sqlalchemy import Column, DateTime, String, Integer, func
import uuid
from sqlalchemy.dialects.postgresql import UUID 
from src.utils.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"