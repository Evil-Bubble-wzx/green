"""
Database connection module for Green Compute System.

Uses SQLAlchemy to create database connection from DATABASE_URL in .env.
Provides engine, SessionLocal, and Base for the application.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env file from project root
# First try the backend's parent directory, then current working directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. "
        "Please create a .env file with your database connection string.\n"
        "Example: DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/green_compute\n"
        "See .env.example for reference."
    )

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
