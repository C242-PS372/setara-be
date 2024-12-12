from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID 
from dataclasses import dataclass
from src.utils.db import db

@dataclass
class Company(db.Model):
    __tablename__ = 'companies'

    id: str
    name: str
    description: str
    created_at: DateTime
    modified_at: DateTime

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    job_listing  = relationship('JobListing', backref='company')

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"