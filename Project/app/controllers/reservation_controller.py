from fastapi import APIRouter, Depends, Request, Form, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.models import get_db, Trip, Reservation
from app.schemas import ReservationCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@router.post("/trips/{trip_id}/reservations")
def add_reservation(
    request: Request,
    trip_id: int,
    title: str = Form(""),
    type: str = Form("other"),
    cost: float = Form(0.0),
    status_val: str = Form("pending", alias="status"),
    db: Session = Depends(get_db)
):
    # Check if trip exists
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Podróż nie została znaleziona")

    errors = []

    try:
        validated_data = ReservationCreate(
            title=title,
            type=type,
            cost=cost,
            status=status_val
        )
    except ValidationError as e:
        for error in e.errors():
            msg = error['msg']
            if "Value error, " in msg:
                msg = msg.replace("Value error, ", "")
            errors.append(msg)

        total_spent = sum(res.cost for res in trip.reservations)
        remaining_budget = trip.budget - total_spent

        return templates.TemplateResponse(
            request=request,
            name="trip_detail.html",
            context={
                "trip": trip,
                "total_spent": total_spent,
                "remaining_budget": remaining_budget,
                "errors": errors,
                "failed_title": title,
                "failed_cost": cost,
                "failed_type": type,
                "failed_status": status_val
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Save to DB
    new_res = Reservation(
        trip_id=trip_id,
        title=validated_data.title,
        type=validated_data.type,
        cost=validated_data.cost,
        status=validated_data.status
    )

    db.add(new_res)
    db.commit()

    return RedirectResponse(f"/trips/{trip_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/reservations/{res_id}/delete")
def delete_reservation(res_id: int, db: Session = Depends(get_db)):
    res = db.query(Reservation).filter(Reservation.id == res_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Rezerwacja nie została znaleziona")

    trip_id = res.trip_id

    db.delete(res)
    db.commit()

    return RedirectResponse(f"/trips/{trip_id}", status_code=status.HTTP_303_SEE_OTHER)

