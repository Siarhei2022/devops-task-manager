import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database connection URL
# The value is provided via environment variable in docker-compose.yml
# Example:
# postgresql+psycopg2://taskapp_user:taskapp_psw@db:5432/taskapp_db
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine for PostgreSQL
# pool_pre_ping=True ensures dead connections are detected and refreshed
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create database session factory 
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all ORM (Object–Relational Mapping) models
# We do not use SQL quiries, instead use objects instead
# This is a base class for all our database entities(see models.py) 
class OrmModelBase(DeclarativeBase):
    pass