*** Settings ***
Documentation  Currently, every endpoint for all microservice (signupsrv, weathersrv, quotesrv)
...  expect some kind of query parameters:
...  - quotesrv: token
...  - signupsrv: username | passwd | user | token
...  - weather: token
...  Not sending the required parameters will yield in `422 Unprocessable Entity` error thrown by FastAPI.
...
...  Let's use a template keyword and verify this for all possible API endpoints for all microservices.
...
...  Should we expand the APIs, it's easy to add the new endpoints to below test cases.
Library         ../resources/keywords.py
Variables       ../resources/variables.py

*** Test Cases ***
quotesrv - Sending no query parameters results in statuscode 422
    [Tags]  negative  quote
    [Template]   Make Request And Expect 422
    GET    quotesrv/quote

signupsrv - Sending no query parameters results in statuscode 422
    [Tags]  negative  signup
    [Template]   Make Request And Expect 422
    POST   signupsrv/signup
    PATCH  signupsrv/renew
    GET    signupsrv/validate
    GET    signupsrv/user

weathersrv - Sending no query parameters results in statuscode 422
    [Tags]  negative  weather
    [Template]   Make Request And Expect 422
    GET    weathersrv/weather