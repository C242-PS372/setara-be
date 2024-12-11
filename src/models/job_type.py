from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID 
from src.utils.db import db

class JobType(db.Model):
    __tablename__ = 'job_types'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    decription = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    job_listing  = relationship('JobListing', backref='job_type')

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"