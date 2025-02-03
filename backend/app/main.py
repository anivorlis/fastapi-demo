import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import groundwater, temperatures

load_dotenv()  # Load variables from .env

HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", 8000))
RELOAD: bool = os.getenv("RELOAD", "True").lower() in ("true", "1", "t")

app = FastAPI()

app.include_router(temperatures.router, prefix="", tags=["Temperatures"])
app.include_router(groundwater.router, prefix="", tags=["Groundwater"])

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD)