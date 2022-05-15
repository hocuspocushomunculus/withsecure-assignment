#!/usr/bin/env python3
"""
Variables used during the robot tests for the WithSecure assignment
"""

BASE_URL = "http://127.0.0.1:8080/api/v1/"
DATABASE = "/opt/be_db.db"

TOKEN_REGEXP = r"[0-9a-fA-F]{32}"

DUMMY_USERNAME_1 = "dummy_username_1"
DUMMY_PASSWORD_1 = "dummy_password_1"

DUMMY_TOKEN = "0" * 31    # One character shorter token than the usual one

DUMMY_USERNAME_2 = "dummy_username_2"
DUMMY_PASSWORD_2 = "dummy_password_2"

QUOTES = [
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

WEATHERS = ["Sunny", "Windy", "Haze", "Mist", "Cloudy", "Rainy", "Hot"]
