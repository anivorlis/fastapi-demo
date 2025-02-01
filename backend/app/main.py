from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv


app = FastAPI()
DATABASE = os.getenv("DATABASE", "data/temperature_data.db")

load_dotenv()  # Load variables from .env

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "True").lower() == "true"

class TemperatureData(BaseModel):
    temperature: float
    location: str
    datetime: datetime

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    conn.close()

def create_database_if_not_exists():
    if not os.path.isdir("data"):
        os.mkdir("data")
    conn = sqlite3.connect(DATABASE)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS temperature (
                temperature REAL,
                location TEXT,
                datetime TEXT
            )
        """)
        conn.commit()
        print("Database and table created (if it didn't exist).")
    except Exception as e:
        print(f"Error creating database/table: {e}")
        conn.rollback()
    finally:
        conn.close()

# Route for reading temperature data by location
@app.get("/temperatures/{location}")
async def get_temperatures_by_location(location: str):
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM temperature WHERE location = ?", (location,))
        rows = cursor.fetchall()
        temperature_data = []
        for row in rows:
            temperature_data.append(TemperatureData(
                temperature=row["temperature"],
                location=row["location"],
                datetime=datetime.fromisoformat(row["datetime"].replace("T", " ")) # Correctly parse datetime
            ))
        close_db_connection(conn)
        return temperature_data
    except Exception as e:
        close_db_connection(conn)
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Route for adding temperature data
@app.post("/temperatures")
async def add_temperature_data(temperature_data: TemperatureData):
    conn = get_db_connection()
    try:
        # Use strftime to format the datetime for SQLite (YYYY-MM-DD HH:MM:SS)
        formatted_datetime = temperature_data.datetime.strftime("%Y-%m-%d %H:%M:%S")

        conn.execute("INSERT INTO temperature (temperature, location, datetime) VALUES (?, ?, ?)",
                     (temperature_data.temperature, temperature_data.location, formatted_datetime))
        conn.commit()
        close_db_connection(conn)
        return {"message": "Temperature data added successfully"}
    except Exception as e:
        conn.rollback()  # Rollback on error
        close_db_connection(conn)
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


if __name__ == "__main__":
    import uvicorn

    create_database_if_not_exists()  # Create the database on startup (if it doesn't exist)
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD)