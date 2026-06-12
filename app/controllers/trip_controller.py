from fastapi import APIRouter, Depends, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import ValidationError

from app.models import get_db, Trip
from app.schemas import TripCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")


@router.get("/", response_class=HTMLResponse)
def list_trips(
    request: Request,
    search: str = "",
    min_budget: str = None,
    max_budget: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Trip)
    
    if search:
        query = query.filter(Trip.destination.like(f"%{search}%"))
        
    min_budget_val = None
    if min_budget is not None and min_budget.strip() != "":
        try:
            min_budget_val = float(min_budget)
            query = query.filter(Trip.budget >= min_budget_val)
        except ValueError:
            pass

    max_budget_val = None
    if max_budget is not None and max_budget.strip() != "":
        try:
            max_budget_val = float(max_budget)
            query = query.filter(Trip.budget <= max_budget_val)
        except ValueError:
            pass
        
    trips = query.order_by(Trip.start_date.asc()).all()
    
    return templates.TemplateResponse(
        request=request,
        name="trip_list.html",
        context={
            "trips": trips,
            "search": search,
            "min_budget": min_budget,
            "max_budget": max_budget
        }
    )


@router.get("/trips/new", response_class=HTMLResponse)
def create_trip_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="trip_form.html",
        context={
            "trip": None,
            "errors": None,
            "form_data": {}
        }
    )


@router.post("/trips/new")
def create_trip(
    request: Request,
    destination: str = Form(""),
    description: str = Form(""),
    start_date_str: str = Form(..., alias="start_date"),
    end_date_str: str = Form(..., alias="end_date"),
    budget: float = Form(0.0),
    image_url: str = Form(""),
    db: Session = Depends(get_db)
):
    errors = []
    start_date = None
    end_date = None
    
    # Parse dates
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        else:
            errors.append("Data rozpoczęcia jest wymagana!")
            
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        else:
            errors.append("Data zakończenia jest wymagana!")
    except ValueError:
        errors.append("Nieprawidłowy format daty. Użyj formatu RRRR-MM-DD")

    form_data = {
        "destination": destination,
        "description": description,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "budget": budget,
        "image_url": image_url
    }

    if errors:
        return templates.TemplateResponse(
            request=request,
            name="trip_form.html",
            context={"trip": None, "errors": errors, "form_data": form_data},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Validation
    try:
        validated_data = TripCreate(
            destination=destination,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            image_url=image_url if image_url.strip() else None
        )
    except ValidationError as e:
        for error in e.errors():
            msg = error['msg']
            if "Value error, " in msg:
                msg = msg.replace("Value error, ", "")
            errors.append(msg)
            
        return templates.TemplateResponse(
            request=request,
            name="trip_form.html",
            context={"trip": None, "errors": errors, "form_data": form_data},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Save to DB
    new_trip = Trip(
        destination=validated_data.destination,
        description=validated_data.description,
        start_date=validated_data.start_date,
        end_date=validated_data.end_date,
        budget=validated_data.budget,
        image_url=validated_data.image_url
    )
    
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/trips/{trip_id}", response_class=HTMLResponse)
def view_trip_detail(request: Request, trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Podróż nie została znaleziona")

    # Budget calculations
    total_spent = sum(res.cost for res in trip.reservations)
    remaining_budget = trip.budget - total_spent

    return templates.TemplateResponse(
        request=request,
        name="trip_detail.html",
        context={
            "trip": trip,
            "total_spent": total_spent,
            "remaining_budget": remaining_budget,
            "errors": None
        }
    )


@router.get("/trips/{trip_id}/edit", response_class=HTMLResponse)
def edit_trip_form(request: Request, trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Podróż nie została znaleziona")
    
    form_data = {
        "destination": trip.destination,
        "description": trip.description,
        "start_date": trip.start_date.isoformat(),
        "end_date": trip.end_date.isoformat(),
        "budget": trip.budget,
        "image_url": trip.image_url or ""
    }

    return templates.TemplateResponse(
        request=request,
        name="trip_form.html",
        context={
            "trip": trip,
            "errors": None,
            "form_data": form_data
        }
    )


@router.post("/trips/{trip_id}/edit")
def edit_trip(
    request: Request,
    trip_id: int,
    destination: str = Form(""),
    description: str = Form(""),
    start_date_str: str = Form(..., alias="start_date"),
    end_date_str: str = Form(..., alias="end_date"),
    budget: float = Form(0.0),
    image_url: str = Form(""),
    db: Session = Depends(get_db)
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Podróż nie została znaleziona")

    errors = []
    start_date = None
    end_date = None
    
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        else:
            errors.append("Data rozpoczęcia jest wymagana!")
            
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        else:
            errors.append("Data zakończenia jest wymagana!")
    except ValueError:
        errors.append("Nieprawidłowy format daty.")

    form_data = {
        "destination": destination,
        "description": description,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "budget": budget,
        "image_url": image_url
    }

    if errors:
        return templates.TemplateResponse(
            request=request,
            name="trip_form.html",
            context={"trip": trip, "errors": errors, "form_data": form_data},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Validation
    try:
        validated_data = TripCreate(
            destination=destination,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            image_url=image_url if image_url.strip() else None
        )
    except ValidationError as e:
        for error in e.errors():
            msg = error['msg']
            if "Value error, " in msg:
                msg = msg.replace("Value error, ", "")
            errors.append(msg)
            
        return templates.TemplateResponse(
            request=request,
            name="trip_form.html",
            context={"trip": trip, "errors": errors, "form_data": form_data},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Update DB
    trip.destination = validated_data.destination
    trip.description = validated_data.description
    trip.start_date = validated_data.start_date
    trip.end_date = validated_data.end_date
    trip.budget = validated_data.budget
    trip.image_url = validated_data.image_url

    db.commit()

    return RedirectResponse(f"/trips/{trip.id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/trips/{trip_id}/delete")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Podróż nie została znaleziona")
        
    db.delete(trip)
    db.commit()
    
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

