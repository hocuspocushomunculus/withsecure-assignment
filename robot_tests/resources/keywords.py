#!/usr/bin/env python3
"""
Common functions to be used across all API robot tests
"""

import re
import sqlite3
import logging
import requests

from variables import BASE_URL, DATABASE, TOKEN_REGEXP

# pylint: disable=invalid-name

# Common & signup_service related keywords
def clean_up_database():
    """
    As a test setup action, remove any users that have been created
    in earlier tests from `be_db.db` sqlite3 database file.
    """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute('''DELETE FROM user;''')

    con.commit()
    con.close()

    logging.info("Successfully cleaned up user database")


def make_request_and_expect_422(request_type: str, endpoint: str) -> None:
    """
    Make a `request_type` request to `endpoint` argument without sending
    any query parameters.
    According to how the APIs for the services have been set up, we
    should expect `422 Unprocessable Entity` if any of the required
    parameters are missing.
    :param request_type:    str, type of the request we'll be making,
                            currently one of: ["GET", "POST", "PATCH"]
    :param endpoint:        str, the endpoint we are making the request to
    """
    if request_type == "GET":
        r = requests.get(BASE_URL + endpoint)
    elif request_type == "POST":
        r = requests.post(BASE_URL + endpoint)
    elif request_type == "PATCH":
        r = requests.patch(BASE_URL + endpoint)

    assert r.status_code == 422, f"Unexpected status code: {r.status_code}"


def sign_up_user_and_return_token(username: str, password: str) -> str:
    """
    Make a valid POST request to `signupsrv/signup` to sign up a new
    user, and return the token.
    :param username:    str, username to use during user registration
    :param password:    str, password to use during user registration
    :return:            str, the hex token that was created for the user
    """
    r = requests.post(BASE_URL + "signupsrv/signup",
                      params={'name': username, 'passwd': password})

    assert r.status_code == 200, f"Unexpected status code: {r.status_code}"

    try:
        token = re.findall(TOKEN_REGEXP, r.content.decode())[0]
        logging.info("Successfully signed up user '%s:%s'", username, password)
    except IndexError:
        raise Exception(f"A token wasn't generated:\n{r.content.decode()}", )

    return token


def user_with_token_exists(username: str, password: str, token: str) -> None:
    """
    Perform an SQL lookup in the user database with given
    `username`, `password` and `token`, we should see an
    entry such as below:
    1	test1 	test1	fcea947770a8039c03b6c9815beb0508

    Raises an exception when a matching entry is not found.
    :param username:    str, username to use in the SQL lookup
    :param password:    str, password to use in the SQL lookup
    :param token:       str, token to use in the SQL lookup
    """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    query = cur.execute(f'''SELECT * FROM user WHERE name="{username}" AND passwd="{password}" AND token="{token}";''')     # pylint: disable=line-too-long
    entries = query.fetchall()

    con.close()

    assert len(entries) == 1, f"Zero or multiple entries returned: {entries}"
    assert entries[0][1] == username, f"Unexpected username returned: '{entries[0][1]}'"
    assert entries[0][2] == password, f"Unexpected password returned: '{entries[0][2]}'"
    assert entries[0][3] == token, f"Unexpected token returned: '{entries[0][3]}'"

    logging.info("Entry '%s' has been found in user database",
                 ('\'' + ' ' * 4 + '\'').join([username, password, token]))


def renew_and_return_token(username: str) -> str:
    """
    Make a PATCH request to `signupsrv/renew` endpoint to renew
    the token for `username` user.
    """
    r = requests.patch(BASE_URL + "signupsrv/renew",
                       params={'name': username})
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}"

    try:
        token = re.findall(TOKEN_REGEXP, r.content.decode())[0]
        logging.info("Successfully renewed token for user '%s'", username)
    except IndexError:
        raise Exception((f"The token for user '{username}' couldn't "
                         f"be renewed:\n{r.content.decode()}"))

    return token


def validate_token(token: str) -> bool:
    """
    Given `token` as the token, make a GET request to `signupsrv/validate`
    endpoint and check if it's a valid token.
    :param token:   str, token to validate
    :return:        bool, true/false depending on the validation result
    """
    r = requests.get(BASE_URL + "signupsrv/validate",
                     params={'token': token})
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}"

    return r.json()


def get_user_by_token(token: str) -> str:
    """
    Given `token` as the token, make a GET request to `signupsrv/user`
    endpont and retrieve the username belonging to the token.
    :param token:   str, token to validate
    :return:        str, user belonging to the supplied token
    """
    r = requests.get(BASE_URL + "signupsrv/user",
                     params={'token': token})
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}"

    return r.json()


# weather_service related keywords
def get_weather(token: str) -> str:
    """
    Given `token` as the token, make a GET request to `weathersrv/weather`
    endpoint and retrieve a random weather.
    :param token:   str, token to pass along
    :return:        str, a random weather returned by the weather_service
                    microservice
    """
    r = requests.get(BASE_URL + "weathersrv/weather",
                     params={'token': token})
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}"

    return r.json()

# quote_service related keywords
def get_quote(token: str) -> str:
    """
    Given `token` as the token, make a GET request to `quotesrv/quote`
    endpoint and retrieve a random quote.
    :param token:   str, token to pass along
    :return:        str, a random quote returned by the quote_service
                    microservice
    """
    r = requests.get(BASE_URL + "quotesrv/quote",
                     params={'token': token})
    assert r.status_code == 200, f"Unexpected status code: {r.status_code}"

    return r.json()
