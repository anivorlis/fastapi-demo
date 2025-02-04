import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load variables from .env

HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", 8000))

API_URL = f"http://{HOST}:{PORT}"

st.title("Groundwater Data Entry and Visualization")

def fetch_locations():
    response = requests.get(f"{API_URL}/groundwaters_locations/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch locations")
        return []

# Fetch available locations
locations = fetch_locations()

# Data Entry Form
level = st.number_input("Enter Groundwater Level", step=0.1)
location = st.text_input("Enter Location")
datetime_input = st.text_input("Enter Datetime (YYYY-MM-DD HH:MM:SS)")

if st.button("Submit"):
    try:
        datetime_obj = datetime.strptime(datetime_input, "%Y-%m-%d %H:%M:%S")
        response = requests.post(f"{API_URL}/groundwater/", json={
            "level": level,
            "location": location,
            "timestamp": datetime_obj.isoformat()
        })
        if response.status_code == 200:
            st.success("Data submitted successfully!")
            # Refetch locations after successful submission
            locations = fetch_locations()
        else:
            st.error(f"Error: {response.json()['detail']}")
    except ValueError:
        st.error("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS.")

# Fetch and Display Data
st.header("Stored Groundwater Data")
selected_location = st.selectbox("Select Location to View Data", locations)
response = requests.get(f"{API_URL}/groundwaters/{selected_location}")
data = response.json()

if data:
    df = pd.DataFrame(data, columns=["level", "location", "timestamp"])
    st.dataframe(df)

    # Plot the data
    st.header("Groundwater Level vs. Datetime")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    fig, ax = plt.subplots()
    df.plot(kind="scatter", x="timestamp", y="level", ax=ax, color='blue', alpha=0.6)
    plt.xlabel("Datetime")
    plt.ylabel("Groundwater Level")
    plt.title(f"Groundwater Level vs. Datetime for {selected_location}")
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)