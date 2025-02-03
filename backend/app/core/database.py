import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()  # Load variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database():
    """Creates the PostgreSQL database and table if they don't exist."""
    # Import all models here to ensure they are included in the metadata
    from app.models.groundwater import GroundwaterMeasurement  # noqa: F401
    from app.models.temperatures import TemperatureData  # noqa: F401
    Base.metadata.create_all(bind=engine)
    print("Database and table created (if they didn't exist).")

def delete_database():
    """Deletes the PostgreSQL database table."""
    # Import all models here to ensure they are included in the metadata
    from app.models.groundwater import GroundwaterMeasurement  # noqa: F401
    from app.models.temperatures import TemperatureData  # noqa: F401
    Base.metadata.drop_all(bind=engine)
    print("Database tables deleted.")