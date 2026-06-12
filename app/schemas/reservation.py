from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal

class ReservationBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Nazwa rezerwacji")
    type: Literal["hotel", "transport", "activity", "other"] = Field(
        "other", 
        description="Typ: hotel, transport, atrakcja lub inne "
    )
    cost: float = Field(0.0, ge=0.0, description="Koszt rezerwacji")
    status: Literal["confirmed", "pending"] = Field("pending", description="Status rezerwacji")

class ReservationCreate(ReservationBase):
    @field_validator("title")
    @classmethod
    def check_title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nazwa rezerwacji nie może składać się wyłącznie ze spacji!")
        return v.strip()

class ReservationResponse(ReservationBase):
    id: int
    trip_id: int
    model_config = ConfigDict(from_attributes=True)

