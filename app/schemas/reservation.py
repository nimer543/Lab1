from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal

class ReservationBase(BaseModel):
    title: str = Field(..., max_length=150, description="Nazwa rezerwacji")
    type: Literal["hotel", "transport", "activity", "other"] = Field(
        "other", 
        description="Typ: hotel, transport, atrakcja lub inne "
    )
    cost: float = Field(0.0, description="Koszt rezerwacji")
    status: Literal["confirmed", "pending"] = Field("pending", description="Status rezerwacji")

class ReservationCreate(ReservationBase):
    @field_validator("title")
    @classmethod
    def check_title_not_empty(cls, v: str) -> str:
        val = v.strip()
        if len(val) < 2:
            raise ValueError("Nazwa rezerwacji musi zawierać co najmniej 2 znaki!")
        return val

    @field_validator("cost")
    @classmethod
    def check_cost(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Koszt rezerwacji nie może być ujemny!")
        return v

class ReservationResponse(ReservationBase):
    id: int
    trip_id: int
    model_config = ConfigDict(from_attributes=True)


