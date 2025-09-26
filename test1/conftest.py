import pytest
import requests
from faker import Faker
from constants import HEADERS, Base_url

faker = Faker()

@pytest.fixture
def booking_auth():
    return {

      "firstname": faker.first_name(),
      "lastname": faker.last_name(),
      "totalprice": faker.random_int(min = 1, max = 500),
      "depositpaid": True,
      "bookingdates": {
        "checkin": "2024-12-20",
        "checkout": "2024-12-25"
      },
      "additionalneeds": "Breakfast"


  }

@pytest.fixture()
def session_auth():
    session = requests.Session()
    session.headers.update(HEADERS)
    response = session.post(f"{Base_url}/auth",json= {"username":"admin","password":"password123"} )
    assert response.status_code == 200, "Статус код не успешный"
    token = response.json().get("token")
    session.headers.update({"cookie":f"token={token}"})
    return session


@pytest.fixture()
def negative_booking():
    return{


            "lastname": faker.last_name(),
            "totalprice": faker.random_int(min=1, max=500),
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-12-20",
                "checkout": "2024-12-25"
            },
            "additionalneeds": "Breakfast"

        }
