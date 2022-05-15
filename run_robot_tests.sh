#!/bin/bash

# 1. Stop any microservices from previous runs
docker ps | grep -o "$(basename $PWD)-.*" | xargs -I container_name docker container rm -f container_name

# 2. Initialize user database and start microservices
touch signup_service/be_db.db
docker compose up -d

# 3. Build Docker container for the robot tests
docker build -f ./Dockerfile_robot -t withsecure_robot_tests .

# 4. Run robot tests in a Docker container
export WORKSPACE="/opt/robot_tests" && \
docker run --rm -it \
--name robot_tests \
--network=host \
-w $WORKSPACE/ \
-v $(pwd)/robot_tests:$WORKSPACE/ \
-v $(pwd)/signup_service/be_db.db:/opt/be_db.db \
withsecure_robot_tests \
robot --outputdir $WORKSPACE/results \
--loglevel DEBUG \
--pythonpath ":.:resources:" ./tests/
