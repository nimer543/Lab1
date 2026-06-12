# app/models/__init__.py

from app.models.database import Base, engine, get_db
from app.models.trip import Trip
from app.models.reservation import Reservation

