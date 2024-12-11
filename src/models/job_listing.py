from sqlalchemy import Column, DateTime, String, Text, ForeignKey, func, Enum as SqlAlchemyEnum
import uuid
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from enum import Enum
from src.utils.db import db

class JobListingStatus(Enum):
    OPEN = 'Open'
    CLOSED = 'Closed'

class JobListing(db.Model):
    __tablename__ = 'job_listings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    job_type_id = Column(UUID(as_uuid=True), ForeignKey('job_types.id'), nullable=False)
    status = Column(SqlAlchemyEnum(
        JobListingStatus, 
        name='status_listing_enum',
        values_callable=lambda obj: [e.value for e in obj]
        ), nullable=False)
    description = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    job_application  = relationship('JobApplication', backref='job_listing')

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"