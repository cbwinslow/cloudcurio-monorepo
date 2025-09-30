from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from typing import Optional

from .config import MCPConfig

# Database setup
DATABASE_URL = MCPConfig.DATABASE_URL or "sqlite:///./crews.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CrewRun(Base):
    __tablename__ = "crew_runs"

    id = Column(Integer, primary_key=True, index=True)
    crew_id = Column(String, unique=True, index=True)
    crew_type = Column(String, index=True)
    status = Column(String, index=True)  # pending, running, completed, failed
    config = Column(JSON)  # Crew configuration
    input_data = Column(JSON)  # Input data for the crew
    result = Column(Text)  # Result/output from the crew
    error = Column(Text)  # Error message if crew failed
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()