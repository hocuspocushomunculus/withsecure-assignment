*** Settings ***
Documentation   Test cases for the signup_service microservice
Library         ../resources/keywords.py
Variables       ../resources/variables.py

Test Setup      Clean Up Database

*** Test Cases ***
POST signup - User can sign up and receive token
    [Documentation]  Sign up a user with dummy credentials and check:
    ...  - If a token is returned
    ...  - If an appropriate entry has been created in the database
    [Tags]  signup  positive
    ${token}=  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    User With Token Exists
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}  token=${token}

POST signup - User cannot sign up with same username
    [Documentation]  Ideally we wouldn't want multiple users to sign up
    ...  with the same username, but currently it is possible.
    [Tags]  signup  negative  bug
    Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    # FIXME: We don't want users successfully registering with the same username
    Run Keyword And Expect Error  *  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

PATCH renew - User can renew his/her token
    [Documentation]  Sign up a user with dummy credentials, and immediately
    ...  renew the token. We should:
    ...  - Find an entry in the database with the renewed token
    ...  - Not find any entries in the database with the old token
    [Tags]  signup  positive
    ${token}=  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    ${new_token}=  Renew And Return Token  username=${DUMMY_USERNAME_1}

    User With Token Exists
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}  token=${new_token}

    # Run a check that there's no entry with the old token
    Run Keyword And Expect Error  Zero*  User With Token Exists
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}  token=${token}

PATCH renew - Non-existent user cannot renew his/her token
    [Documentation]  If a user hasn't signed up previously, arbitrary usernames
    ...  should get denied by the `signupsrv/renew` endpoint.
    ...
    ...  Omitting the signup step, let's try to renew the token for a user
    ...  that doesn't exist in the database. We should get an error.
    [Tags]  signup  negative
    Run Keyword And Expect Error  *404  Renew And Return Token  username=${DUMMY_USERNAME_1}

GET validate - Existing token should receive a validation of true
    [Documentation]  Sign up a user and try to validate the received token.
    ...  For a valid token we should receive `true` as a response
    [Tags]  signup  positive
    ${token}=  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    ${validation_result}=  Validate Token  token=${token}
    Should Be Equal  ${validation_result}  ${TRUE}

GET validate - Non-existent token should receive a validation of false
    [Documentation]  Starting with an empty database and trying to
    ...  validate a token through the `signupsrv/validate` endpoint,
    ...  we should receive `false` as a response.
    [Tags]  signup  negative
    ${validation_result}  Validate Token  token=${DUMMY_TOKEN}
    Should Be Equal  ${validation_result}  ${FALSE}

GET user - Querying with token belonging to first user returns first user in the database
    [Documentation]  Signing up a user and then making a GET request to `signupsrv/user`
    ...  endpoint and passing the generated token along should return the user.
    [Tags]  signup  positive
    ${token}=  Sign Up User And Return Token
        ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    ${user}=  Get User By Token  token=${token}
    Should Be Equal  ${user}  ${DUMMY_USERNAME_1}

GET user - Querying with token belonging to any but the first user returns the expected user
    [Documentation]  Signing up 2 users with different credentials and then
    ...  making a GET request to `signupsrv/user` endpoint and passing the token
    ...  for the second user along should return the second user.
    ...
    ...  Currently the API always returns the username of the first user in the database.
    [Tags]  signup  positive  bug
    # Sign up first user
    ${token_1}=  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_1}  password=${DUMMY_PASSWORD_1}

    # Sign up second user
    ${token_2}=  Sign Up User And Return Token
    ...  username=${DUMMY_USERNAME_2}  password=${DUMMY_PASSWORD_2}

    # FIXME: We should get the 2nd user back, but we don't
    ${user}=  Get User By Token  token=${token_2}
    Should Be Equal  ${user}  ${DUMMY_USERNAME_2}

GET user - Invalid token returns statuscode 400
    [Documentation]  Making a GET request to `signupsrv/user` and passing along
    ...  an invalid token (e.g. a token which doesn't exist in the user database),
    ...  we should get an error with statuscode 400.
    [Tags]  signup  negative  bug
    # FIXME: Currently we're receiving statuscode 401 which isn't according to the documentation
    Run Keyword And Expect Error  *400  Get User By Token  token=${DUMMY_TOKEN}
