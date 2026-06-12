from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, default="other")
    cost = Column(Float, default=0.0)
    status = Column(String, default="pending")

    trip = relationship("Trip", back_populates="reservations")

