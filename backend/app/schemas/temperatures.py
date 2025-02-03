from datetime import datetime

from pydantic import BaseModel


class TemperatureDataBase(BaseModel):
    temperature: float
    location: str
    datetime: datetime

class TemperatureDataCreate(TemperatureDataBase):
    pass

class TemperatureDataResponse(TemperatureDataBase):
    class Config:
        from_attributes = True