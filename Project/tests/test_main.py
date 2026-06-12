import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, get_db

# RAM database setup
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)

# Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "TravelPlanner MVC"}


def test_list_trips_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Moje podróże" in response.text


def test_create_trip_validation_failure():
    form_data = {
        "destination": "Rzym, Włochy",
        "description": "Wycieczka do Koloseum",
        "start_date": "2026-06-15",
        "end_date": "2026-06-10",
        "budget": 500.0,
        "image_url": ""
    }
    response = client.post("/trips/new", data=form_data)
    
    assert response.status_code == 400
    assert "Data zakończenia podróży nie może być wcześniejsza niż data rozpoczęcia!" in response.text


def test_create_trip_success():
    form_data = {
        "destination": "Paryż, Francja",
        "description": "Zobaczyć Wieżę Eiffla",
        "start_date": "2026-07-01",
        "end_date": "2026-07-10",
        "budget": 1200.0,
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"
    }
    response = client.post("/trips/new", data=form_data, follow_redirects=False)
    
    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_add_reservation_success():
    # 1. Create a trip
    client.post("/trips/new", data={
        "destination": "Tokio, Japonia",
        "start_date": "2026-08-01",
        "end_date": "2026-08-15",
        "budget": 3000.0
    })

    # 2. Add reservation
    res_data = {
        "title": "Hotel Capsule Ryokan Tokyo",
        "type": "hotel",
        "cost": 450.00,
        "status": "confirmed"
    }
    response = client.post("/trips/1/reservations", data=res_data, follow_redirects=False)
    
    assert response.status_code == 303
    assert response.headers["location"] == "/trips/1"


def test_list_trips_empty_query_params():
    response = client.get("/?search=&min_budget=&max_budget=")
    assert response.status_code == 200
    assert "Moje podróże" in response.text

