from sqlalchemy import Column, DateTime, String, Integer, Enum, func
import uuid
from sqlalchemy.dialects.postgresql import UUID 
from src.utils.db import db

# class AgeEnum(Enum):
#     AGE_17_24 = '17-24'
#     AGE_25_30 = '25-30'
#     AGE_31_35 = '31-35'

# class ExperienceEnum(Enum):
#     EXPERIENCE_0_2 = '0-2'
#     EXPERIENCE_3_5 = '3-5'
#     EXPERIENCE_6 = '6'

# class DisabilityEnum(Enum):
#     DAKSA = "Daksa"
#     RUNGU = "Rungu"
#     NETRA = "Netra"

# class CityEnum(Enum):
#     JAKARTA = 'Jakarta'
#     BANDUNG = 'Bandung'
#     BOGOR = 'Bogor'
#     DEPOK = 'Depok'
#     BEKASI = 'Bekasi'
#     CIMAHI = 'Cimahi'
#     TANGERANG = 'Tangerang'
#     SUKABUMI = 'Sukabumi'
#     TASIKMALAYA = 'Tasikmalaya'
#     CIREBON = 'Cirebon'
#     SUMEDANG = 'Sumedang'
#     PURWAKARTA = 'Purwakarta'
#     GARUT = 'Garut'
#     CIAMIS = 'Ciamis'



class User(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    gender = Column(String(50), nullable=True)
    age = Column(String(50), nullable=True)
    experience = Column(String(50), nullable=True)
    disability = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"