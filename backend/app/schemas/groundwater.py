from datetime import datetime

from pydantic import BaseModel


class GroundwaterMeasurementCreate(BaseModel):
    level: float
    location: str
    timestamp: datetime

class GroundwaterMeasurementResponse(BaseModel):
    id: int
    level: float
    location: str
    timestamp: datetime

    class Config:
        from_attributes = True