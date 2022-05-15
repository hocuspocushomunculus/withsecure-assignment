*** Settings ***
Documentation   Test cases for the weather_service microservice
Library         Collections
Library         ../resources/keywords.py
Variables       ../resources/variables.py

Test Setup      Clean Up Database

*** Test Cases ***
GET weather - Sending valid token yields random weather
    [Documentation]  Sign up a user and use the generated token
    ...  and make a GET request to the `weathersrv/weather` endpoint to
    ...  get a random weather.
    [Tags]  weather  positive
    ${token}=  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    ${weather}=  Get Weather  token=${token}

    List Should Contain Value  ${WEATHERS}  ${weather}

GET weather - Sending invalid or empty token is rejected
    [Documentation]  Without signing up a user, make a GET request to the
    ...  `weathersrv/weather` endpoint while passing along a bogus token.
    ...  Ideally we should not get back any weather as a response, but
    ...  our request should get denied.
    [Tags]  weather  negative  bug
    # FIXME: there's no token validation, we can get a weather with an empty token
    Run Keyword And Expect Error  *  Get Weather  token=${EMPTY}
