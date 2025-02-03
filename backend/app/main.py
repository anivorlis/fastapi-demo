import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import temperatures

load_dotenv()  # Load variables from .env

HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", 8000))
RELOAD: bool = os.getenv("RELOAD", "True").lower() in ("true", "1", "t")

app = FastAPI()
for pypath in sys.path:
    print(pypath)

app.include_router(temperatures.router, prefix="", tags=["Temperatures"])

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD)