from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.orm import relationship
from app.models.database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, default=0.0)
    image_url = Column(String, nullable=True)

    reservations = relationship("Reservation", back_populates="trip", cascade="all, delete-orphan")

