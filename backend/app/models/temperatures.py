from sqlalchemy import Column, DateTime, Float, String

from app.core.database import Base


class TemperatureData(Base):
    __tablename__ = "temperature"

    temperature = Column(Float, primary_key=True, index=True)
    location = Column(String, primary_key=True, index=True)
    datetime = Column(DateTime, primary_key=True, index=True)