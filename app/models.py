from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from .config import settings
from .utils import logger

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


# Database engine
engine = create_async_engine(settings.database_url, echo=True)

# Session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


def create_tables():
    try:
        # Create tables in the database using the models defined
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error(f"Error occurred while creating tables: {str(e)}")
        raise e
