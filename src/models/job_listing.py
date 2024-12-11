from sqlalchemy import Column, DateTime, String, Text, ForeignKey, func, Enum
import uuid
from sqlalchemy.dialects.postgresql import UUID 
from src.utils.db import db

class JobListing(db.Model):
    __tablename__ = 'job_listing'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    job_type_id = Column(UUID(as_uuid=True), ForeignKey('job_types.id'), nullable=False)
    status = Column(Enum('Open', 'Closed', name='status_listing_enum'), nullable=False)
    description = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"