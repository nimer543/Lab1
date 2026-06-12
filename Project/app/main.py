# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.models import Base, engine
from app.controllers import trip_router, reservation_router

app = FastAPI()

# Database init
Base.metadata.create_all(bind=engine)

# Static files
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "views", "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Routers
app.include_router(trip_router)
app.include_router(reservation_router)

# Health check
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "TravelPlanner MVC"}

