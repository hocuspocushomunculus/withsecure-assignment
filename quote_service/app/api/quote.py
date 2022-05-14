from typing import Optional

from fastapi import APIRouter, FastAPI, HTTPException
import random, os, httpx

SIGNUP_SERVICE_LOCALHOST_URL = "http://127.0.0.1:8001/api/v1/signupsrv"
signup_url = os.environ.get("SIGNUP_SERVICE_URL", SIGNUP_SERVICE_LOCALHOST_URL)

quote = APIRouter()

quotes = [
    "Responsive is better than fast",
    "It’s not fully shipped until it’s fast",
    "Anything added dilutes everything else",
    "Practicality beats purity",
    "Approachable is better than simple",
    "Mind your words, they are important",
    "Speak like a human",
    "Half measures are as bad as nothing at all",
    "Encourage flow",
    "Non-blocking is better than blocking",
    "Favor focus over features",
]


@quote.get("/quote", summary="Generates quote")
def random_quote(token: str):
    """
    Returns Random Quote

    - **token**: Valid token to fetch quote
    """
    print(f"SignupUrl::{signup_url}")
    r = httpx.get(f"{signup_url}/validate?token={token}")
    print(f"Status Code::{r.status_code}")
    if r.status_code == 200:
        is_token_validate: bool = r.json()
        print(f"Json Value::{is_token_validate}")
        if not is_token_validate:
            raise HTTPException(status_code=401, detail="token is invalid")
    return random.choice(quotes)
