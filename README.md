# Bowling Events API

This is a backend service that interacts with [Bowling Events UI](https://github.com/lorenzotan/bowling_events_ui).

## Description

## Getting Started
```shell
$ docker build -t bowl:api .
$ docker-compose up -d
$ fastapi run main.py
$ curl -v http://localhost:8000/
```

## Tech Stack
* Python
* FastAPI
* Alembic
* SQLModel
* PostgreSQL

## Version History
* [0.2.0](https://github.com/lorenzotan/bowling_events_api/tree/0.2.0): Read/Write Locations and Events
* [0.1.0](https://github.com/lorenzotan/bowling_events_api/tree/0.1.0): FastAPI init