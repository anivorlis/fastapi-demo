from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.groundwater import GroundwaterMeasurement
from app.schemas.groundwater import (
    GroundwaterMeasurementCreate,
    GroundwaterMeasurementResponse,
)

router = APIRouter()

@router.post("/groundwater/", response_model=GroundwaterMeasurementResponse)
async def create_groundwater_measurement(measurement: GroundwaterMeasurementCreate, db: Session = Depends(get_db)):
    try:
        db_measurement = GroundwaterMeasurement(**measurement.model_dump())
        db.add(db_measurement)
        db.commit()
        db.refresh(db_measurement)
        return db_measurement  # Return the created data
    except Exception as e:
        db.rollback()  # Rollback if there's an error
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
@router.get("/groundwaters/", response_model=List[GroundwaterMeasurementResponse])
async def get_all_groundwater_measurements(db: Session = Depends(get_db)):
    try:
        measurements = db.query(GroundwaterMeasurement).all()
        return measurements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
@router.get("/groundwaters/{location}", response_model=List[GroundwaterMeasurementResponse])
async def get_groundwater_measurements_by_location(location: str, db: Session = Depends(get_db)):
    try:
        measurements = db.query(GroundwaterMeasurement).filter(GroundwaterMeasurement.location == location).all()
        if not measurements:
            raise HTTPException(status_code=404, detail="No data found for the specified location")
        return measurements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
@router.get("/groundwaters_locations/", response_model=List[str])
async def get_positions(db: Session = Depends(get_db)):
    try:
        positions = db.query(GroundwaterMeasurement.location).distinct().all()
        return [position[0] for position in positions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")