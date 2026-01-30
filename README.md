# Online Cinema API

A backend service for an Online Cinema platform built with FastAPI, SQLAlchemy, Alembic, PostgreSQL, Docker, and Poetry.

This project provides a RESTful API for managing movies, users, authentication, and related cinema entities. It is designed as a production-ready backend with migrations, containerization, and modern Python tooling.

## Tech Stack:
- Python 3.11+ (local) / 3.14 (Docker image)

- FastAPI — web framework

- SQLAlchemy 2.0 — ORM

- Alembic — database migrations

- PostgreSQL — database

- Poetry — dependency management

- Docker & Docker Compose — containerization

- Uvicorn — ASGI server

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/NazarSerdiuk1/Online-cinema-fastapi.git

2. Navigate to the project folder:
    ```bash
    cd online_cinema_prodject
    ```
3. Virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate      # Windows
    source venv/bin/activate  # Linux/Mac
    ```
4. Install dependencies:
    ```bash
    pip install poetry
    poetry install
    ```    ```

## Run with Docker
1. Build containers
    ```bash
        docker-compose build --no-cache
    ```
2. Start the application
    ```bash
        docker-compose up
    ```
