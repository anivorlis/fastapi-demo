import math
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.database import create_database, delete_database, get_db
from app.models.temperatures import TemperatureData
from app.schemas.temperatures import TemperatureDataCreate


def generate_temperature_data(location="Location1", year=2024, month=1, day=1):
    """Generates hourly temperature data for a specific day."""

    target_date = datetime(year, month, day, 0, 0)  # Start of the target day
    end_date = target_date + timedelta(days=1)  # End of the target day (exclusive)
    current_date = target_date

    data = []
    while current_date < end_date:  # Important: < not <= to avoid the first hour of the next day
        # Base temperature (between 10 and 15)
        base_temp = random.uniform(10, 15)

        # Small sinusoidal variation (simulating daily changes - adjust period if needed)
        hour_of_day = current_date.hour
        sin_variation = math.sin(2 * math.pi * hour_of_day / 24) * 0.5  # Smaller amplitude for daily variation

        # Small random noise
        noise = random.uniform(-0.2, 0.2)  # Reduced noise level

        temperature = base_temp + sin_variation + noise
        data.append(TemperatureDataCreate(temperature=temperature, location=location, datetime=current_date))
        current_date += timedelta(hours=1)

    return data

def store_temperature_data(data, db: Session):
    location = data[0].location  # Assuming all data is for the same location
    try:
        # Clear previous data for the same location
        db.query(TemperatureData).filter(TemperatureData.location == location).delete()
        db.commit()  # Commit the delete operation

        # Insert new data
        db_temperature_data = [TemperatureData(**item.model_dump()) for item in data]
        db.add_all(db_temperature_data)
        db.commit()
        print(f"Inserted {len(data)} records.")
    except Exception as e:
        db.rollback()  # Rollback if there's an error
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    delete_database()
    create_database()
    db = next(get_db())
    store_temperature_data(generate_temperature_data(location="AMS"), db)
    store_temperature_data(generate_temperature_data(location="UTR"), db)
    print("Temperature data generation and storage complete.")