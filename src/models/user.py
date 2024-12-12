from sqlalchemy import Column, DateTime, String, Enum as SqlAlchemyEnum, func
import uuid
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from src.utils.db import db

class GenderEnum(Enum):
    MALE = 'Male'
    FEMALE = 'Female'

class AgeEnum(Enum):
    AGE_17_24 = '17-24'
    AGE_25_30 = '25-30'
    AGE_31_35 = '31-35'

class ExperienceEnum(Enum):
    EXPERIENCE_0_2 = '0-2'
    EXPERIENCE_3_5 = '3-5'
    EXPERIENCE_6 = '6'

class DisabilityEnum(Enum):
    DAKSA = "Daksa"
    RUNGU = "Rungu"
    NETRA = "Netra"

class CityEnum(Enum):
    JAKARTA = 'Jakarta'
    BANDUNG = 'Bandung'
    BOGOR = 'Bogor'
    DEPOK = 'Depok'
    BEKASI = 'Bekasi'
    CIMAHI = 'Cimahi'
    TANGERANG = 'Tangerang'
    SUKABUMI = 'Sukabumi'
    TASIKMALAYA = 'Tasikmalaya'
    CIREBON = 'Cirebon'
    SUMEDANG = 'Sumedang'
    PURWAKARTA = 'Purwakarta'
    GARUT = 'Garut'
    CIAMIS = 'Ciamis'

@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: str
    name: str
    username: str
    password: str
    email: str
    gender: str
    age: str
    experience: str
    disability: str
    city: str
    created_at: DateTime
    modified_at: DateTime

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    gender = Column(SqlAlchemyEnum(
        GenderEnum,
        name='gender_enum',
        values_callable=lambda obj: [e.value for e in obj]
    ), nullable=True)
    age = Column(SqlAlchemyEnum(
        AgeEnum,
        name='age_enum',
        values_callable=lambda obj: [e.value for e in obj]
    ), nullable=True)
    experience = Column(SqlAlchemyEnum(
        ExperienceEnum,
        name='experience_enum',
        values_callable=lambda obj: [e.value for e in obj]
    ), nullable=True)
    disability = Column(SqlAlchemyEnum(
        DisabilityEnum,
        name='disability_enum',
        values_callable=lambda obj: [e.value for e in obj]
    ), nullable=True)
    city = Column(SqlAlchemyEnum(
        CityEnum,
        name='city_enum',
        values_callable=lambda obj: [e.value for e in obj]
    ), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    job_application  = relationship('JobApplication', backref='user')

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"