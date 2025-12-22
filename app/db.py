# Database configuration and session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Database connection string from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://dev:dev@db:5432/devdb",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for ORM models
class Base(DeclarativeBase):
    pass

