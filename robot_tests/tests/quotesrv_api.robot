*** Settings ***
Documentation   Test cases for the quote_service microservice
Library         Collections
Library         ../resources/keywords.py
Variables       ../resources/variables.py

Test Setup      Clean Up Database

*** Test Cases ***
GET quote - Sending valid token yields random quote
    [Documentation]  Sign up a user and use the generated token
    ...  and make a GET request to the `quotesrv/quote` endpoint to
    ...  get a random quote.
    [Tags]  quote  positive
    ${token}=  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    ${quote}=  Get Quote  token=${token}

    List Should Contain Value  ${QUOTES}  ${quote}

GET quote - Sending invalid or empty token is rejected
    [Documentation]  Without signing up a user, make a GET request to the
    ...  `quotesrv/quote` endpoint while passing along a bogus token.
    ...  Ideally we should not get back any quote as a response, but
    ...  our request should get denied.
    [Tags]  quote  negative
    Run Keyword And Expect Error  *401  Get Quote  token=${EMPTY}
