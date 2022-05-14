# Introduction

There are 3 microservices that are running when the backend is up. Here is a brief description of the services

- Signup service -- Service for user to create his account. After account is created a token is returned. This token is needed to access other two services. If one forgets his token, he can renew his token.
- Quote service -- Quotation service. This generates random quotes. One will need to provide token provided by the signup service
- Weather service -- Weather service. This generates random weather. One will need to provide token provided by the signup service

## How to run services

All the services are containerised. Hence you will need docker to be installed already on your system.

If you do not have it installed on your machine, you can download it from [here](https://www.docker.com/products/docker-desktop).

Once docker is running, follow these steps --

From the root of the folder run following command in terminal `docker-compose up -d`.

You can now find 3 services running at the apis running at --

- http://127.0.0.1:8001/api/v1/signupsrv
- http://127.0.0.1:8080/api/v1/quotesrv
- http://127.0.0.1:8080/api/v1/weathersrv

Documentation for the apis can be found at -

- http://127.0.0.1:8001/api/v1/signupsrv/docs
- http://127.0.0.1:8080/api/v1/quotesrv/docs
- http://127.0.0.1:8080/api/v1/weathersrv/docs

You can inspect user's database using [DB Browser for SQLite](https://sqlitebrowser.org/).
Database named `be_db.db` is generated under signup_service

## Assignment

- Your task is to write api tests for all 3 services
- You are free to choose tool/library and language of your choice, we prefer python inside our team.
- If you find any bug, please write a bug report which can help developer identify problem and fix it.
  (If you find multiple bugs/problems, create a bug report for one of the many you found. But mention other bugs that you discovered)
- Please send link to your code in github.
- Add relevant documentation to the sources and information on how to run your tests.
