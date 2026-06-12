from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from datetime import date
from typing import Optional

class TripBase(BaseModel):
    destination: str = Field(..., max_length=100, description="Cel podróży")
    description: Optional[str] = Field(None, max_length=1000, description="Opis podróży")
    start_date: date = Field(..., description="Data rozpoczęcia podróży")
    end_date: date = Field(..., description="Data zakończenia podróży")
    budget: float = Field(0.0, description="Budżet podróży")
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
        val = v.strip()
        if len(val) < 2:
            raise ValueError("Cel podróży musi zawierać co najmniej 2 znaki!")
        return val

    @field_validator("budget")
    @classmethod
    def check_budget(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Budżet podróży nie może być ujemny!")
        return v

class TripUpdate(TripCreate):
    pass

class TripResponse(TripBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


