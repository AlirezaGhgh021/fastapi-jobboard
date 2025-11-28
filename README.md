# FastAPI JobBoard – My First Real Backend Project (and it's a fucking beast)

A complete, production-ready job board API built from scratch with **FastAPI + PostgreSQL + JWT + Docker**.

I survived:
- Alembic hell
- Docker networking wars on Linux
- 100+ errors in one day
- Swagger's file upload tantrums
- And still shipped this monster

## Features (ALL WORKING)

- User register / login with JWT
- Create your company
- Post unlimited jobs
- Apply to jobs with PDF resume upload
- View your applications
- Duplicate apply protection
- Clean async SQLModel + Alembic migrations
- Dockerized PostgreSQL
- Swagger UI with working Bearer auth

## Tech Stack

- FastAPI (async)
- SQLModel + PostgreSQL
- JWT authentication
- Alembic migrations
- Docker + docker-compose
- Secure password hashing (bcrypt)
- File upload (PDF resumes)

## Quick Start

```bash
# Clone and enter
git clone https://github.com/AlirezaGhgh021/fastapi-jobboard.git
cd fastapi-jobboard

# Start DB
docker compose up -d db

# Install & run
poetry install
alembic upgrade head
poetry run uvicorn jobboard_api.main:app --reload