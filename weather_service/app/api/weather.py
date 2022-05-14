from fastapi import APIRouter
import random, os, httpx

SIGNUP_SERVICE_LOCALHOST_URL = "http://localhost:8002/signupsrv"
signup_url = os.environ.get("SIGNUP_SERVICE_URL", SIGNUP_SERVICE_LOCALHOST_URL)
weather = APIRouter()

weathers = ["Sunny", "Windy", "Haze", "Mist", "Cloudy", "Rainy", "Hot"]


@weather.get("/weather", summary="Returns weather")
def random_weather(token: str):
    """
    Gets weather against a valid token

    - **token**: Valid token to access weather information
    """
    r = httpx.get(f"{signup_url}/validate?token={token}")
    if r.status_code == 200:
        is_token_validate: bool = r.json()
        print(f"Json Value::{is_token_validate}")
    return random.choice(weathers)
