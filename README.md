# withsecure-assignment

Repository containing the write-up for the WithSecure Assignment:
- How the [repository](#repository-tree) looks like
- How to [start the services manually](#start-services)
- Some [useful SQL commands](#useful-sql-commands) for manual testing
- The [test plan](#test-plan)
- How to [run the API tests](#run-api-tests)
- **The [bug report](#bug-report) section detailing the bugs that were observed (and some RCA)**

**Operating system used: Linux 20.04 Ubuntu**

# Repository tree

```text
.
├── assignment_readme.md
├── docker-compose.yml
├── Dockerfile_robot
├── nginx_config.conf
├── quote_service
│   ├── app
│   │   ├── api
│   │   │   └── quote.py
│   │   └── main.py
│   ├── dockerfile
│   └── requirements.txt
├── README.md
├── robot_tests
│   ├── resources
│   │   ├── lib_common.py
│   │   ├── lib_quotesrv.py
│   │   ├── lib_signupsrv.py
│   │   ├── lib_weathersrv.py
│   │   └── variables.py
│   ├── results
│   │   ├── log.html
│   │   ├── output.xml
│   │   └── report.html
│   └── tests
│       ├── quotesrv_api.robot
│       ├── signupsrv_api.robot
│       └── weathersrv_api.robot
├── signup_service
│   ├── app
│   │   ├── api
│   │   │   ├── be_db
│   │   │   │   ├── database.py
│   │   │   │   ├── db_api.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── models.py
│   │   │   └── signup.py
│   │   └── main.py
│   ├── dockerfile
│   └── requirements.txt
└── weather_service
    ├── app
    │   ├── api
    │   │   └── weather.py
    │   └── main.py
    ├── dockerfile
    └── requirements.txt
```

# Start services

For performing manual and exploratory testing (check [here](#bug-report) to see more info about the [[MAJOR BUG]](#1-major-bug-when-starting-docker-containers-as-is) mentioned below)

```bash
# Build and start docker containers (with a slight deviation from the assignment's original instructions)
# The slight deviation being: we create the database file owned by our user (e.g.: daniel:daniel & 664),
# otherwise it would be created by Docker with root:root & 644 permissions and cause some confusion.
# >>> For more info about what confusion it would cause, see the `Bug report` section <<<
touch signup_service/be_db.db
docker compose up -d

# Inspect the started containers
docker ps

# To stop and clean up the containers:
docker ps | grep -o "$(basename $PWD)-.*" | xargs -I container_name docker container rm -f container_name
```

# Useful SQL commands 

For inspecting `user` database during manual and exploratory testing

```sql
-- 1. Open `be_db.db` with sqlitebrowser

-- 2. List all users
SELECT * FROM user;

-- 3. Clean up user (example)
DELETE FROM user WHERE name=="test";
```

# Test plan:

## QuoteAPI - GET /api/v1/quotesrv/quote (token)
- Sending no token should result in `422 Unprocessable Entity`
- Valid token results in 200 - random quote
- Invalid token throws 401 error

## SignupAPI - POST /api/v1/signupsrv/signup (name & password)
- Sending no username and/or password should result in `422 Unprocessable Entity`
- User can sign up (and get token of length 33)
- [[MINOR BUG]](#3-minor-bug-for-post-apiv1signupsrvsignup-endpoint) User cannot sign up with same username (user can actually sign up again with same username)

## SignupAPI - PATCH /api/v1/signupsrv/renew (name)
- Sending no token should result in `422 Unprocessable Entity`
- User can renew his/her token
- Non-existent user cannot renew any tokens

## SignupAPI - GET /api/v1/signupsrv/validate (token)
- Sending no token should result in `422 Unprocessable Entity`
- Existing token should receive a validation of `true`
- Non-existent token should receive a validation of `false`

## SignupAPI - GET /api/v1/signupsrv/user (token)
- Sending no token should result in `422 Unprocessable Entity`
- Token belonging to first user returns first user in the database
- [[MAJOR BUG]](#4-major-bug-for-get-apiv1signupsrvuser-endpoint) Token belonging to any other user returns the user the token belongs to (any other valid token always returns the first user)
- [[MINOR BUG]](#5-minor-bug-for-get-apiv1signupsrvuser-endpoint) Invalid token returns "Invalid token" (returns 401, should be 400 according to documentation)

## WeatherAPI - GET /api/v1/weathersrv/weather (token)
- Sending no token should result in `422 Unprocessable Entity`
- Valid token results in 200 - random weather
- [[MAJOR BUG]](#6-major-bug-for-get-apiv1weathersrvweather-endpoint) Invalid token is rejected (Improper token validation: any token is accepted, even empty one)

# Run API tests

## 1. Build Docker container for robot tests

```bash
docker build -f ./Dockerfile_robot -t withsecure_robot_tests .
```

## 2. Run robot tests in a Docker container

```bash
export WORKSPACE="/opt/robot_tests" && \
docker run --rm -it \
--name robot_tests \
--network=host \
-w $WORKSPACE/ \
-v $(pwd)/robot_tests:$WORKSPACE/ \
withsecure_robot_tests \
robot --outputdir $WORKSPACE/results \
--loglevel INFO \
--pythonpath ":.:resources:" ./tests/
```

# Bug report

## 1. [MAJOR] bug when starting docker containers as is

If the containers are started solely with the `docker compose up -d` command, the database file `signup_service/be_db.db` will be created with permissions `root:root & 644` (i.e. no write permissions for our user).

Implications:
- We would be able to make POST requests to the `/api/v1/signupsrv/signup` endpoint and create new users
- However after making a PATCH request to the `/api/v1/signupsrv/renew` endpoint, neither can we renew the tokens, nor can we create any more users:
  - `/api/v1/signupsrv/renew` endpoint will throw `400 bad request`
  - `/api/v1/signupsrv/signup` endpoint will throw `500 internal server error`

There are multiple ways to deal with this problem:

### Solution 1: Restart the signup service Docker container

```bash
# Stop and remove signup service
docker container rm -f withsecure-assignment-signup_service-1

# Add read-write permissions to the db file for anonymous users (== our user outside Docker)
chmod 666 signup_service/be_db.db

# Restart signup service
docker compose up -d signup_service
```

### Solution 2: Configure same read-write permissions at start-up

```python
# Inside `signup_service/app/api/be_db/database.py` include below line
# for `create_db_and_tables` function:
import subprocess; subprocess.run(["chmod", "666", sqlite_file_name])
```

### Solution 3: Creating the database file before starting any of the services

(We are actually using this workaround for the robot tests)

```bash
touch signup_service/be_db.db  # This will create the database and will be owned by our user
docker compose up -d
```

## 2. [MINOR] bug in the original readme file

In original README:

http://127.0.0.1:8001/api/v1/signupsrv 

Should have been using port 8080 (as for the other services' URLs):

http://127.0.0.1:8080/api/v1/signupsrv

## 3. [MINOR] bug for `POST /api/v1/signupsrv/signup` endpoint

User can sign up multiple times using the same username.

This could be bad if we didn't want the user to have multiple active tokens.

## 4. [MAJOR] bug for `GET /api/v1/signupsrv/user` endpoint

We can send any valid tokens in the request, but we'll always get the first user created in the `user` database. There's currently no way of getting any of the users present in the database.

## 5. [MINOR] bug for `GET /api/v1/signupsrv/user` endpoint

Although the documentation lists [200, 400, 404] as possible status codes for the response, 
however when passing an invalid token along with the request will yield a response 
with status code 401, which isn't according to the documentation.

## 6. [MAJOR] bug for `GET /api/v1/weathersrv/weather` endpoint

There's no proper validation for tokens made to the `/api/v1/weathersrv/weather` endpoint.

Root cause analysis: We are happy with the status code of 200 received after making a request to `/api/v1/signupsrv/validate` endpoint. We aren't checking if the response body was true or false.
