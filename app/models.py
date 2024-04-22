from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from .config import settings


Base = declarative_base()


class CustomBase(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])


class Repository(CustomBase):
    __tablename__ = settings.tablename  # Use settings to define table name
    id = Column(Integer, primary_key=True)
    full_name = Column(String, index=True, unique=True)
    description = Column(String)
    clone_url = Column(String)
    stars = Column(Integer)  # stargazers_count
    created_at = Column(DateTime)
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ttl = Column(Float, default=3600.0)  # TTL in seconds
