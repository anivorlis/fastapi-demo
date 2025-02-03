import os
import uuid
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.filehandler.temperatures import write_data_to_csv
from app.models.temperatures import TemperatureData
from app.schemas.temperatures import TemperatureDataCreate, TemperatureDataResponse

router = APIRouter()

@router.get("/temperatures/test")
async def test():
    return {"message": "Test successful"}

@router.get("/temperatures/{location}", response_model=List[TemperatureDataResponse])
async def get_temperatures_by_location(location: str, db: Session = Depends(get_db)):
    try:
        rows = db.query(TemperatureData).filter(TemperatureData.location == location).all()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get("/temperatures/{location}/csv")
async def download_temperature_data_by_location(background_tasks: BackgroundTasks, location: str, db: Session = Depends(get_db)):
    file_path = f"temperature_data_{location}_{uuid.uuid4()}.csv"
    data = db.query(TemperatureData).filter(TemperatureData.location == location).all()
    write_data_to_csv(data, file_path)
    response = FileResponse(path=file_path, filename=file_path, media_type='application/octet-stream')
    response.headers["Content-Disposition"] = f"attachment; filename={file_path}"

    # Use a background task to delete the file after the response is sent
    def delete_file(path: str):
        os.remove(path)

    background_tasks.add_task(delete_file, file_path)

    return response

@router.post("/temperatures/", response_model=TemperatureDataResponse)
async def create_temperature(temperature_data: TemperatureDataCreate, db: Session = Depends(get_db)):
    try:
        db_temperature_data = TemperatureData(**temperature_data.dict())
        db.add(db_temperature_data)
        db.commit()
        db.refresh(db_temperature_data)
        return db_temperature_data  # Return the created data
    except Exception as e:
        db.rollback()  # Rollback if there's an error
        raise HTTPException(status_code=500, detail=f"Database error: {e}")