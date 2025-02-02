import math
import os
import random
import sqlite3
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

# Database configuration
DATABASE = os.getenv("DATABASE", "data/temperature_data.db")


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
        data.append((temperature, location, current_date.isoformat()))
        current_date += timedelta(hours=1)

    return data


def delete_database():
    """Deletes the SQLite database file."""
    try:
        os.remove(DATABASE)
        print(f"Database file '{DATABASE}' deleted.")
    except FileNotFoundError:
        print(f"Database file '{DATABASE}' not found.  Nothing to delete.")
    except Exception as e:
        print(f"Error deleting database file: {e}")


def create_database():
    """Creates the SQLite database and table if they don't exist."""
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
        print("Database and table created (if they didn't exist).")
    except Exception as e:
        print(f"Error creating database/table: {e}")
        conn.rollback() # Rollback in case of an error
    finally:
        conn.close()


def store_temperature_data(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    location = data[0][1]  # Assuming all data is for the same location
    try:
        cursor.execute(f"DELETE FROM temperature WHERE location = '{location}'") # Clear previous data for the same location
        conn.commit() # commit the delete

        cursor.executemany("INSERT INTO temperature (temperature, location, datetime) VALUES (?, ?, ?)", data)
        conn.commit()
        print(f"Inserted {len(data)} records.")
    except Exception as e:
        conn.rollback()  # Rollback if there's an error
        print(f"Error inserting data: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    delete_database()
    create_database()
    store_temperature_data(generate_temperature_data(location="AMS"))
    store_temperature_data(generate_temperature_data(location="UTR"))
    print("Temperature data generation and storage complete.")