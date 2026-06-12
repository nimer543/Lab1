from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from datetime import date
from typing import Optional

class TripBase(BaseModel):
    destination: str = Field(..., min_length=2, max_length=100, description="Cel podróży")
    description: Optional[str] = Field(None, max_length=1000, description="Opis podróży")
    start_date: date = Field(..., description="Data rozpoczęcia podróży")
    end_date: date = Field(..., description="Data zakończenia podróży")
    budget: float = Field(0.0, ge=0.0, description="Budżet podróży (nie może być ujemny)")
    image_url: Optional[str] = Field(None, description="Link do zdjęcia")

class TripCreate(TripBase):
    @model_validator(mode="after")
    def check_dates(self) -> 'TripCreate':
        if self.end_date < self.start_date:
            raise ValueError("Data zakończenia podróży nie może być wcześniejsza niż data rozpoczęcia!")
        return self

    @field_validator("destination")
    @classmethod
    def check_destination_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Cel podróży nie może składać się wyłącznie ze spacji!")
        return v.strip()

class TripUpdate(TripCreate):
    pass

class TripResponse(TripBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

