from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base


class GroundwaterMeasurement(Base):
    __tablename__ = "groundwater_level"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)